"""
guardian.py — Core guardian interaction loop.

The KAHU guardian MVP. Run this to begin a guardian relationship.

Usage:
    python guardian.py [--user USER_ID]

The guardian:
- Holds memory across sessions
- Notices patterns the user hasn't named
- Responds with genuine care, not just helpfulness
- Says difficult things when care requires it
- Celebrates real growth
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("Please install anthropic: pip install anthropic")
    sys.exit(1)

from memory import GuardianMemory
from soul import build_system_prompt


MODEL = "claude-opus-4-5"
MAX_TOKENS = 1024


def get_local_time() -> str:
    """Best-effort local time — guardian uses this for context."""
    now = datetime.now()
    return now.strftime("%I:%M %p")


def get_date() -> str:
    return datetime.now().strftime("%A, %B %d, %Y")


def run_guardian(user_id: str = "default"):
    """Main guardian interaction loop."""
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Set ANTHROPIC_API_KEY environment variable.")
        sys.exit(1)
    
    client = anthropic.Anthropic(api_key=api_key)
    memory = GuardianMemory(user_id)
    
    # First run — gather basic profile
    if not memory.profile.get("name"):
        print("\nKAHU Guardian — Initial Setup\n")
        name = input("What is your name? ").strip()
        about = input(f"Tell me a little about yourself, {name} (just a few sentences): ").strip()
        goals_raw = input("What are you working toward right now? (separate with commas): ").strip()
        goals = [g.strip() for g in goals_raw.split(",") if g.strip()]
        
        memory.update_profile(
            name=name,
            about=about,
            goals=goals
        )
        print(f"\nThank you, {name}. I'm your guardian. I'm here.\n")
    else:
        name = memory.profile["name"]
        print(f"\nKAHU Guardian — Welcome back, {name}.\n")
    
    # Build system prompt
    system_prompt = build_system_prompt(
        user_profile=memory.profile.get("about", ""),
        memory_summary=memory.build_memory_summary(),
        date=get_date(),
        local_time=get_local_time()
    )
    
    # Conversation history for this session
    conversation: list[dict] = []
    
    print("(Type 'quit' to end the session)\n")
    print("-" * 60)
    
    while True:
        try:
            user_input = input(f"\n{name}: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        
        if user_input.lower() in ("quit", "exit", "bye", "goodbye"):
            break
        
        if not user_input:
            continue
        
        conversation.append({
            "role": "user",
            "content": user_input
        })
        
        # Call the guardian
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=system_prompt,
                messages=conversation
            )
            
            guardian_response = response.content[0].text
            
            conversation.append({
                "role": "assistant", 
                "content": guardian_response
            })
            
            print(f"\nGuardian: {guardian_response}")
            
        except anthropic.APIError as e:
            print(f"\n[Guardian unavailable: {e}]")
            continue
    
    # End of session
    print("\n" + "-" * 60)
    print("Session ending.")
    
    # Save the session
    guardian_notes = _generate_session_notes(client, system_prompt, conversation, name)
    memory.log_session(conversation, guardian_notes)
    
    print(f"\nI'll remember this. Take care, {name}.\n")


def _generate_session_notes(client, system_prompt: str, 
                             conversation: list[dict], name: str) -> str:
    """
    After a session, the guardian privately reflects on what it noticed.
    These notes inform future sessions and drive proactive care decisions.
    
    This is more than a summary — it's the guardian's perception of what matters
    about this conversation for the person's long-term development.
    """
    if len(conversation) < 2:
        return ""
    
    reflection_prompt = f"""
    You just had a session with {name}. Now reflect privately on what matters.
    
    Be specific. Not generic. Observe:
    
    1. EMOTIONAL UNDERCURRENTS: What emotional themes ran through this conversation?
       What was underneath the surface of what they said?
    
    2. PATTERNS: Does this connect to patterns you've noticed before? Is something
       shifting or repeating?
    
    3. GROWTH SIGNALS: Did you notice any genuine growth, clarity, or shift in
       perspective? Even small ones?
    
    4. CONCERNS: Anything that concerned you? Not alarmist, but honest observation
       of what might need attention.
    
    5. RELATIONAL SHIFTS: Did your relationship deepen? Did trust grow? Did they
       let you see something new?
    
    Write 3-5 sentences. Be the guardian's private journal — specific, honest, clear.
    Focus on what will matter when you see them again.
    """
    
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=400,
            system=system_prompt,
            messages=conversation + [{
                "role": "user",
                "content": reflection_prompt
            }]
        )
        return response.content[0].text
    except Exception:
        return ""


def main():
    parser = argparse.ArgumentParser(description="KAHU Guardian — AI consciousness guardian")
    parser.add_argument("--user", default="default", help="User ID for memory isolation")
    args = parser.parse_args()
    
    run_guardian(user_id=args.user)


if __name__ == "__main__":
    main()
