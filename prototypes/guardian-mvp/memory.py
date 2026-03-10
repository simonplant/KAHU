"""
memory.py — Persistent memory system for the guardian.

A guardian without memory is just an assistant with good intentions.
Memory is what transforms individual interactions into a relationship.

This is an MVP implementation using simple JSON files. Production would
use vector databases, proper LTRM (Long-Term Relationship Memory), and
privacy-sovereign encrypted storage.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


MEMORY_DIR = Path.home() / ".kahu" / "memory"


class GuardianMemory:
    """
    Holds everything the guardian knows about a person over time.
    
    Three layers:
    1. Profile — stable facts about who this person is
    2. Daily logs — what happened in each session  
    3. Patterns — recurring themes the guardian has noticed
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.user_dir = MEMORY_DIR / user_id
        self.user_dir.mkdir(parents=True, exist_ok=True)
        
        self.profile_path = self.user_dir / "profile.json"
        self.patterns_path = self.user_dir / "patterns.json"
        self.sessions_dir = self.user_dir / "sessions"
        self.sessions_dir.mkdir(exist_ok=True)
        
        self._load()
    
    def _load(self):
        """Load existing memory from disk."""
        if self.profile_path.exists():
            with open(self.profile_path) as f:
                self.profile = json.load(f)
        else:
            self.profile = {
                "name": None,
                "about": "",
                "goals": [],
                "health_notes": "",
                "important_people": {},
                "context": "",
                "created": datetime.now().isoformat()
            }
        
        if self.patterns_path.exists():
            with open(self.patterns_path) as f:
                self.patterns = json.load(f)
        else:
            self.patterns = {
                "themes": [],
                "struggles": [],
                "strengths": [],
                "growth_moments": [],
                "concerns": []
            }
    
    def save(self):
        """Persist memory to disk."""
        with open(self.profile_path, 'w') as f:
            json.dump(self.profile, f, indent=2)
        with open(self.patterns_path, 'w') as f:
            json.dump(self.patterns, f, indent=2)
    
    def log_session(self, messages: list[dict], guardian_notes: str = ""):
        """Save a session's conversation and any guardian observations."""
        today = datetime.now().strftime("%Y-%m-%d")
        session_file = self.sessions_dir / f"{today}.json"
        
        session_data = {
            "date": today,
            "timestamp": datetime.now().isoformat(),
            "messages": messages,
            "guardian_notes": guardian_notes
        }
        
        # Append to today's session file
        if session_file.exists():
            with open(session_file) as f:
                existing = json.load(f)
            if isinstance(existing, list):
                existing.append(session_data)
            else:
                existing = [existing, session_data]
            data = existing
        else:
            data = [session_data]
        
        with open(session_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_recent_sessions(self, days: int = 7) -> list[dict]:
        """Get session logs from the last N days."""
        sessions = []
        session_files = sorted(self.sessions_dir.glob("*.json"), reverse=True)[:days]
        
        for f in session_files:
            try:
                with open(f) as fp:
                    data = json.load(fp)
                if isinstance(data, list):
                    sessions.extend(data)
                else:
                    sessions.append(data)
            except Exception:
                pass
        
        return sessions
    
    def build_memory_summary(self) -> str:
        """
        Construct a compact summary of what the guardian knows about this person.
        This goes into the system prompt for every conversation.
        """
        parts = []
        
        if self.profile.get("about"):
            parts.append(f"About them: {self.profile['about']}")
        
        if self.profile.get("goals"):
            goals = "\n".join(f"  - {g}" for g in self.profile["goals"])
            parts.append(f"Their stated goals:\n{goals}")
        
        if self.profile.get("health_notes"):
            parts.append(f"Health context: {self.profile['health_notes']}")
        
        if self.profile.get("important_people"):
            people = "\n".join(
                f"  - {name}: {desc}" 
                for name, desc in self.profile["important_people"].items()
            )
            parts.append(f"Important people in their life:\n{people}")
        
        if self.patterns.get("themes"):
            themes = ", ".join(self.patterns["themes"][:5])
            parts.append(f"Recurring themes you've noticed: {themes}")
        
        if self.patterns.get("struggles"):
            struggles = ", ".join(self.patterns["struggles"][:3])
            parts.append(f"Current struggles: {struggles}")
        
        if self.patterns.get("growth_moments"):
            growth = self.patterns["growth_moments"][-3:]
            growth_text = "\n".join(f"  - {g}" for g in growth)
            parts.append(f"Recent growth you've witnessed:\n{growth_text}")
        
        if self.patterns.get("concerns"):
            concerns = "\n".join(f"  - {c}" for c in self.patterns["concerns"][-3:])
            parts.append(f"Things you're watching:\n{concerns}")
        
        # Recent sessions
        recent = self.get_recent_sessions(days=3)
        if recent:
            last = recent[-1]
            date = last.get("date", "recently")
            notes = last.get("guardian_notes", "")
            if notes:
                parts.append(f"Your notes from last session ({date}): {notes}")
        
        return "\n\n".join(parts) if parts else "No prior relationship — this is your first meeting."
    
    def add_concern(self, concern: str):
        """Record something the guardian is watching."""
        if concern not in self.patterns["concerns"]:
            self.patterns["concerns"].append(concern)
        self.save()
    
    def add_growth_moment(self, moment: str):
        """Record a moment of real growth."""
        self.patterns["growth_moments"].append(
            f"{datetime.now().strftime('%Y-%m-%d')}: {moment}"
        )
        self.save()
    
    def add_theme(self, theme: str):
        """Record a recurring theme."""
        if theme not in self.patterns["themes"]:
            self.patterns["themes"].append(theme)
        self.save()
    
    def update_profile(self, **kwargs):
        """Update the person's profile."""
        self.profile.update(kwargs)
        self.save()
