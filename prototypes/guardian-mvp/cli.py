"""
cli.py — Command-line interface for the KAHU guardian.

Provides a clean CLI for managing the guardian relationship:
- guardian start — begin or resume a session
- guardian memory — view memory and patterns
- guardian report — get a summary of recent activity
- guardian update-profile — update profile information
- guardian list-users — manage multiple guardian relationships
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

from memory import GuardianMemory
from guardian import run_guardian, get_date, get_local_time
from patterns import EmotionalPatternRecognizer
from proactive import ProactiveCareEngine


def cmd_start(args):
    """Start a new session or resume an existing one."""
    user_id = args.user or "default"
    run_guardian(user_id=user_id)


def cmd_memory(args):
    """View memory and patterns for the user."""
    user_id = args.user or "default"
    memory = GuardianMemory(user_id)
    
    print(f"\n📖 Memory for {memory.profile.get('name', 'Unknown')}\n")
    print("-" * 60)
    
    # Profile
    print("\n📝 Profile:")
    if memory.profile.get("about"):
        print(f"  About: {memory.profile['about']}")
    
    if memory.profile.get("goals"):
        print("  Goals:")
        for goal in memory.profile["goals"]:
            print(f"    • {goal}")
    
    if memory.profile.get("health_notes"):
        print(f"  Health: {memory.profile['health_notes']}")
    
    if memory.profile.get("important_people"):
        print("  Important people:")
        for person, desc in memory.profile["important_people"].items():
            print(f"    • {person}: {desc}")
    
    # Patterns
    print("\n🔄 Patterns Noticed:")
    if memory.patterns.get("themes"):
        print("  Themes:")
        for theme in memory.patterns["themes"][:5]:
            print(f"    • {theme}")
    
    if memory.patterns.get("struggles"):
        print("  Current struggles:")
        for struggle in memory.patterns["struggles"][:5]:
            print(f"    • {struggle}")
    
    if memory.patterns.get("strengths"):
        print("  Strengths:")
        for strength in memory.patterns["strengths"][:5]:
            print(f"    • {strength}")
    
    if memory.patterns.get("growth_moments"):
        print("  Recent growth:")
        for moment in memory.patterns["growth_moments"][-3:]:
            print(f"    • {moment}")
    
    if memory.patterns.get("concerns"):
        print("  Concerns being watched:")
        for concern in memory.patterns["concerns"][-3:]:
            print(f"    ⚠️  {concern}")
    
    # Recent sessions
    recent = memory.get_recent_sessions(days=7)
    if recent:
        print(f"\n📅 Recent sessions ({len(recent)} in the last week)")
        for session in recent[-5:]:  # Last 5
            date = session.get("date", "?")
            msg_count = len(session.get("messages", []))
            notes = session.get("guardian_notes", "")
            summary = notes[:60] + "..." if len(notes) > 60 else notes
            print(f"  {date}: {msg_count} messages | {summary}")
    
    print("\n" + "-" * 60 + "\n")


def cmd_report(args):
    """Generate a summary report of guardian relationship status."""
    user_id = args.user or "default"
    memory = GuardianMemory(user_id)
    
    name = memory.profile.get("name", "User")
    print(f"\n📊 Guardian Report for {name}\n")
    print("=" * 60)
    
    # Relationship duration
    created = memory.profile.get("created", "unknown")
    if created != "unknown":
        created_date = datetime.fromisoformat(created)
        duration = datetime.now() - created_date
        days = duration.days
        print(f"\n⏱️  Relationship Duration: {days} days")
    
    # Session frequency
    recent_sessions = memory.get_recent_sessions(days=30)
    if recent_sessions:
        print(f"📅 Sessions in last 30 days: {len(recent_sessions)}")
        avg_per_week = len(recent_sessions) / (max(1, duration.days) / 7)
        print(f"   Average per week: {avg_per_week:.1f}")
    
    # Themes over time
    themes = memory.patterns.get("themes", [])
    if themes:
        print(f"\n🔄 Primary themes:")
        for theme in themes[:5]:
            print(f"   • {theme}")
    
    # Growth tracking
    growth = memory.patterns.get("growth_moments", [])
    if growth:
        print(f"\n🌱 Growth moments recorded: {len(growth)}")
        print("   Recent:")
        for moment in growth[-3:]:
            print(f"   • {moment}")
    
    # Current focus areas
    struggles = memory.patterns.get("struggles", [])
    if struggles:
        print(f"\n⚠️  Current focus areas:")
        for struggle in struggles[:3]:
            print(f"   • {struggle}")
    
    # Health and wellness
    if memory.profile.get("health_notes"):
        print(f"\n💪 Health context: {memory.profile['health_notes']}")
    
    # Next steps
    print(f"\n➡️  Next Steps:")
    print(f"   • Continue building trust and understanding")
    if recent_sessions:
        last_session = recent_sessions[-1]
        last_date = datetime.fromisoformat(last_session.get("timestamp", datetime.now().isoformat()))
        hours_ago = (datetime.now() - last_date).total_seconds() / 3600
        if hours_ago > 48:
            print(f"   • Consider reaching out (last contact {hours_ago:.0f} hours ago)")
    print(f"   • Deepen memory of patterns and preferences")
    print(f"   • Notice and celebrate growth moments")
    
    print("\n" + "=" * 60 + "\n")


def cmd_update_profile(args):
    """Update the user's profile."""
    user_id = args.user or "default"
    memory = GuardianMemory(user_id)
    
    print(f"\n✏️  Update profile for {memory.profile.get('name', 'User')}\n")
    
    # Name
    name = input(f"Name [{memory.profile.get('name', '')}]: ").strip()
    if name:
        memory.profile["name"] = name
    
    # About
    about = input(f"About you [{memory.profile.get('about', '')[:40]}...]: ").strip()
    if about:
        memory.profile["about"] = about
    
    # Goals
    if input("Update goals? (y/n): ").lower() == "y":
        goals_raw = input("Goals (comma-separated): ").strip()
        goals = [g.strip() for g in goals_raw.split(",") if g.strip()]
        memory.profile["goals"] = goals
    
    # Health
    health = input(f"Health notes [{memory.profile.get('health_notes', '')[:40]}...]: ").strip()
    if health:
        memory.profile["health_notes"] = health
    
    # Important people
    if input("Update important people? (y/n): ").lower() == "y":
        important_people = {}
        while True:
            person = input("Person's name (or 'done'): ").strip()
            if person.lower() == "done":
                break
            desc = input(f"Relationship to {person}: ").strip()
            important_people[person] = desc
        memory.profile["important_people"] = important_people
    
    memory.save()
    print(f"\n✅ Profile updated.\n")


def cmd_list_users(args):
    """List all users with active guardian relationships."""
    memory_dir = Path.home() / ".kahu" / "memory"
    
    if not memory_dir.exists():
        print("\n📭 No guardian relationships yet.\n")
        return
    
    users = [d.name for d in memory_dir.iterdir() if d.is_dir()]
    
    if not users:
        print("\n📭 No guardian relationships yet.\n")
        return
    
    print(f"\n👥 Guardian Relationships ({len(users)})\n")
    print("-" * 60)
    
    for user_id in sorted(users):
        try:
            memory = GuardianMemory(user_id)
            name = memory.profile.get("name", user_id)
            sessions = memory.get_recent_sessions(days=365)
            created = memory.profile.get("created", "unknown")
            
            if created != "unknown":
                created_date = datetime.fromisoformat(created)
                duration = (datetime.now() - created_date).days
                duration_str = f"{duration} days"
            else:
                duration_str = "unknown"
            
            print(f"📌 {name}")
            print(f"   ID: {user_id}")
            print(f"   Duration: {duration_str}")
            print(f"   Sessions: {len(sessions)}")
            print()
        except Exception as e:
            print(f"   Error reading {user_id}: {e}\n")
    
    print("-" * 60 + "\n")


def cmd_analyze(args):
    """Analyze emotional patterns in recent sessions."""
    user_id = args.user or "default"
    memory = GuardianMemory(user_id)
    
    name = memory.profile.get("name", "User")
    print(f"\n🧠 Emotional Pattern Analysis for {name}\n")
    print("-" * 60)
    
    # Analyze recent sessions
    recognizer = EmotionalPatternRecognizer()
    recent = memory.get_recent_sessions(days=7)
    
    for session in recent:
        messages = session.get("messages", [])
        for msg in messages:
            if msg.get("role") == "user":
                content = msg.get("content", "")
                analysis = recognizer.analyze_text(content)
    
    # Report
    themes = recognizer.get_recurring_themes()
    
    if themes.get("frequent_states"):
        print("\n🎭 Frequent emotional states:")
        for state, count in sorted(themes["frequent_states"].items(), key=lambda x: x[1], reverse=True):
            print(f"   • {state} ({count} times)")
    
    if themes.get("recurring_concerns"):
        print("\n⚠️  Recurring concerns:")
        for concern, count in sorted(themes["recurring_concerns"].items(), key=lambda x: x[1], reverse=True):
            print(f"   • {concern.replace('_', ' ')} ({count} times)")
    
    should_prompt, prompt_topic = recognizer.should_gentle_prompt()
    if should_prompt:
        print(f"\n💭 Potential check-in topic:")
        print(f"   {prompt_topic}")
    
    summary = recognizer.generate_pattern_summary()
    if summary:
        print(f"\n📝 Summary: {summary}")
    
    print("\n" + "-" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="KAHU Guardian — AI consciousness guardian CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  guardian start                    # Start a session
  guardian start --user john        # Session as john
  guardian memory                   # View memory and patterns
  guardian report                   # Get a summary report
  guardian update-profile           # Update your profile
  guardian analyze                  # Analyze emotional patterns
  guardian list-users               # List all relationships
        """
    )
    
    parser.add_argument(
        "--user",
        default="default",
        help="User ID for memory isolation (default: 'default')"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # start
    subparsers.add_parser(
        "start",
        help="Start a new session or resume existing one"
    )
    
    # memory
    subparsers.add_parser(
        "memory",
        help="View memory, patterns, and relationship history"
    )
    
    # report
    subparsers.add_parser(
        "report",
        help="Generate a summary report of guardian relationship"
    )
    
    # update-profile
    subparsers.add_parser(
        "update-profile",
        help="Update your profile information"
    )
    
    # analyze
    subparsers.add_parser(
        "analyze",
        help="Analyze emotional patterns in recent sessions"
    )
    
    # list-users
    subparsers.add_parser(
        "list-users",
        help="List all guardian relationships"
    )
    
    args = parser.parse_args()
    
    # If no command specified, default to start
    if not args.command:
        cmd_start(args)
        return
    
    # Route to appropriate command
    command_handlers = {
        "start": cmd_start,
        "memory": cmd_memory,
        "report": cmd_report,
        "update-profile": cmd_update_profile,
        "analyze": cmd_analyze,
        "list-users": cmd_list_users,
    }
    
    handler = command_handlers.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
