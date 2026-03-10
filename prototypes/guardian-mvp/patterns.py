"""
patterns.py — Emotional pattern recognition for the guardian.

The guardian's ability to notice patterns is what transforms it from an assistant
into something that feels like genuine care. This module detects emotional states,
tracks recurring themes, and flags concerns that might not be obvious to the person
themselves.
"""

import re
from datetime import datetime
from collections import Counter
from typing import Optional


class EmotionalPatternRecognizer:
    """
    Analyzes text to detect emotional states and track patterns over time.
    
    This is intentionally simple — not a black-box classifier, but interpretable
    pattern matching that can be explained to the user: "I notice you've mentioned
    feeling overwhelmed in three conversations now. That's worth paying attention to."
    """
    
    # Emotional state keywords — recognizable, not comprehensive
    EMOTIONAL_STATES = {
        "overwhelmed": ["overwhelmed", "swamped", "drowning", "can't keep up", "too much"],
        "anxious": ["anxious", "nervous", "worried", "stressed", "tense", "on edge"],
        "depressed": ["depressed", "hopeless", "numb", "empty", "pointless", "what's the point"],
        "frustrated": ["frustrated", "irritated", "annoyed", "fed up", "exasperated"],
        "energized": ["energized", "excited", "motivated", "pumped", "ready"],
        "calm": ["calm", "peaceful", "centered", "grounded", "at peace"],
        "confused": ["confused", "unclear", "don't know", "lost", "disoriented"],
        "lonely": ["alone", "isolated", "lonely", "disconnected", "no one understands"],
        "grateful": ["grateful", "thankful", "appreciate", "blessed", "lucky"],
        "proud": ["proud", "accomplished", "achieved", "did it", "made it"],
    }
    
    # Behavioral patterns that might indicate issues
    CONCERN_PATTERNS = {
        "isolation": ["alone", "don't want to see anyone", "staying in", "withdrawn"],
        "substance_reliance": ["drinking more", "using more", "can't sleep without", "dependent on"],
        "self_criticism": ["my fault", "i'm the problem", "i'm broken", "i'm worthless", "i never"],
        "avoidance": ["not dealing with", "ignoring", "avoiding", "pretending it's fine"],
        "rumination": ["can't stop thinking about", "keep replaying", "same thought again"],
        "sleep_issues": ["can't sleep", "sleeping too much", "tired all the time", "exhausted"],
        "appetite_changes": ["not eating", "eating everything", "food just", "nothing tastes"],
        "concentration_issues": ["can't focus", "brain fog", "concentration gone", "scattered"],
    }
    
    def __init__(self):
        self.patterns_detected = {}
        self.state_history = []
        self.concerns_detected = []
    
    def analyze_text(self, text: str) -> dict:
        """
        Analyze a piece of text for emotional content and patterns.
        Returns a dict of detected states, patterns, and any concerns.
        """
        text_lower = text.lower()
        
        detected_states = self._detect_emotional_states(text_lower)
        detected_concerns = self._detect_concerns(text_lower)
        intensity = self._estimate_emotional_intensity(text, detected_states)
        
        result = {
            "primary_states": detected_states,
            "concerns": detected_concerns,
            "intensity": intensity,
            "timestamp": datetime.now().isoformat(),
        }
        
        self.state_history.append(result)
        return result
    
    def _detect_emotional_states(self, text: str) -> list[str]:
        """Find emotional states mentioned in the text."""
        detected = []
        for state, keywords in self.EMOTIONAL_STATES.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text):
                    detected.append(state)
                    break
        return detected
    
    def _detect_concerns(self, text: str) -> list[str]:
        """Identify concerning patterns that might warrant attention."""
        concerns = []
        for concern_type, patterns in self.CONCERN_PATTERNS.items():
            for pattern in patterns:
                if re.search(r'\b' + re.escape(pattern) + r'\b', text):
                    concerns.append(concern_type)
                    break
        return list(set(concerns))  # Remove duplicates
    
    def _estimate_emotional_intensity(self, text: str, states: list[str]) -> str:
        """
        Rough intensity estimate based on exclamation marks, caps, repetition.
        Returns: "low", "moderate", "high"
        """
        exclamations = text.count("!")
        all_caps_words = len(re.findall(r'\b[A-Z]{2,}\b', text))
        repetition = len(text) - len(set(text.split()))  # Rough measure
        
        if exclamations > 2 or all_caps_words > 3:
            return "high"
        elif exclamations > 0 or all_caps_words > 1:
            return "moderate"
        else:
            return "low"
    
    def get_recurring_themes(self, num_recent: int = 10) -> dict:
        """
        Identify what emotional themes are showing up repeatedly.
        Useful for the guardian to notice patterns the person might not see.
        """
        if not self.state_history:
            return {}
        
        recent = self.state_history[-num_recent:]
        
        # Count emotional states
        all_states = []
        for session in recent:
            all_states.extend(session.get("primary_states", []))
        
        # Count concerns
        all_concerns = []
        for session in recent:
            all_concerns.extend(session.get("concerns", []))
        
        state_counts = Counter(all_states)
        concern_counts = Counter(all_concerns)
        
        return {
            "frequent_states": dict(state_counts.most_common(3)),
            "recurring_concerns": dict(concern_counts.most_common(3)),
            "sessions_analyzed": len(recent),
        }
    
    def generate_pattern_summary(self) -> str:
        """
        Generate a natural language summary of patterns for the guardian to use.
        This is what the guardian might say: "I've noticed X showing up repeatedly."
        """
        if not self.state_history:
            return ""
        
        themes = self.get_recurring_themes()
        
        parts = []
        
        if themes.get("frequent_states"):
            states = ", ".join(themes["frequent_states"].keys())
            parts.append(f"I've been noticing you mention {states} fairly regularly.")
        
        if themes.get("recurring_concerns"):
            concerns = list(themes["recurring_concerns"].keys())
            if len(concerns) == 1:
                parts.append(f"One thing I'm keeping an eye on: {concerns[0].replace('_', ' ')}.")
            else:
                concern_list = ", ".join(c.replace('_', ' ') for c in concerns[:2])
                parts.append(f"A few things I'm noticing: {concern_list}.")
        
        return " ".join(parts)
    
    def get_concern_flags(self) -> list[str]:
        """
        Returns any significant concerns that the guardian should be aware of.
        Used internally for protective instincts.
        """
        if not self.state_history:
            return []
        
        # Check last 5 sessions
        recent = self.state_history[-5:]
        
        concern_counts = Counter()
        for session in recent:
            for concern in session.get("concerns", []):
                concern_counts[concern] += 1
        
        # Flag concerns that appear in 3+ of last 5 sessions
        significant_concerns = [
            concern for concern, count in concern_counts.items() if count >= 3
        ]
        
        return significant_concerns
    
    def should_gentle_prompt(self) -> tuple[bool, Optional[str]]:
        """
        Determine if the guardian should gently bring something up.
        Returns (should_prompt, suggested_topic)
        
        This is the protective instinct: noticing something might need
        a gentle inquiry, but not being pushy about it.
        """
        flags = self.get_concern_flags()
        
        if not flags:
            return (False, None)
        
        # Pick the most recurring concern
        most_common = flags[0]
        
        prompt_mapping = {
            "isolation": "I've noticed you mentioning feeling alone. How are you doing with that?",
            "substance_reliance": "I want to check in gently — have you noticed any patterns with your usage?",
            "self_criticism": "You've been pretty hard on yourself. Worth reminding you that you're doing your best.",
            "rumination": "That thought keeps coming back. Sometimes it helps to shift perspective.",
            "sleep_issues": "Sleep seems to be rough. That affects everything else. What would help?",
            "concentration_issues": "Your focus feels scattered. That's a sign you might need to ease up.",
        }
        
        if most_common in prompt_mapping:
            return (True, prompt_mapping[most_common])
        
        return (True, f"I'm noticing something about {most_common.replace('_', ' ')}.")
    
    def reset(self):
        """Clear history — useful for testing or when starting with a new user."""
        self.patterns_detected = {}
        self.state_history = []
        self.concerns_detected = []
