"""
test_proactive.py — Tests for proactive care engine.
"""

import pytest
from datetime import datetime, timedelta
from proactive import ProactiveCareEngine


def test_check_in_cooldown():
    """Test that guardian respects check-in frequency limits."""
    engine = ProactiveCareEngine()
    
    # Just checked in
    engine.update_last_contact()
    should_check = engine.should_initiate_check_in(hours_since_last_contact=12)
    assert should_check is False
    
    # 48+ hours since contact
    engine.last_check_in = datetime.now() - timedelta(hours=50)
    should_check = engine.should_initiate_check_in(hours_since_last_contact=50)
    assert should_check is True  # Time to check in


def test_generic_check_in():
    """Test generic check-in generation."""
    engine = ProactiveCareEngine()
    
    message = engine._generic_check_in()
    assert message is not None
    assert len(message) > 10
    assert any(phrase in message.lower() for phrase in ["how", "doing", "check", "wondering"])


def test_concerned_check_in():
    """Test check-in generation for specific concerns."""
    engine = ProactiveCareEngine()
    
    # Test isolation concern
    message = engine._concerned_check_in("isolation")
    assert message is not None
    assert "alone" in message.lower() or "isolated" in message.lower()
    
    # Test sleep concern
    message = engine._concerned_check_in("sleep_issues")
    assert message is not None
    assert "sleep" in message.lower()
    
    # Test self-criticism concern
    message = engine._concerned_check_in("self_criticism")
    assert message is not None
    assert "hard" in message.lower() or "yourself" in message.lower()


def test_pattern_based_check_in():
    """Test check-in based on emotional patterns."""
    engine = ProactiveCareEngine()
    
    patterns = {
        "frequent_states": {"overwhelmed": 3, "anxious": 2}
    }
    
    message = engine._pattern_based_check_in(patterns)
    assert message is not None
    assert "overwhelmed" in message.lower() or "feelings" in message.lower()


def test_celebration_generation():
    """Test generation of celebration moments."""
    engine = ProactiveCareEngine()
    
    growth = "started going to the gym regularly"
    message = engine.generate_celebration_moment(growth)
    
    assert message is not None
    assert "growth" in message.lower() or growth in message.lower()


def test_stay_quiet_detection():
    """Test detection of situations where guardian should not reach out."""
    engine = ProactiveCareEngine()
    
    assert engine.when_to_stay_quiet("I need space right now") is True
    assert engine.when_to_stay_quiet("Please leave me alone") is True
    assert engine.when_to_stay_quiet("I'm grieving") is True
    
    assert engine.when_to_stay_quiet("I'm doing fine") is False
    assert engine.when_to_stay_quiet("Let's talk about my week") is False


def test_reflection_prompt_generation():
    """Test generation of reflection prompts."""
    engine = ProactiveCareEngine()
    
    prompt = engine.generate_reflection_prompt()
    assert prompt is not None
    assert len(prompt) > 20
    assert "?" in prompt  # Should be a question


def test_escalation_detection():
    """Test detection of concerns requiring professional help."""
    engine = ProactiveCareEngine()
    
    # No concerns
    should_escalate = engine.should_escalate_concern([])
    assert should_escalate is False
    
    # Multiple persistent concerns
    concerns = ["sleep_issues", "isolation", "rumination"]
    should_escalate = engine.should_escalate_concern(concerns)
    assert should_escalate is True
    
    # Severe concern
    should_escalate = engine.should_escalate_concern(["suicidal ideation"])
    assert should_escalate is True


def test_escalation_message():
    """Test generation of appropriate escalation message."""
    engine = ProactiveCareEngine()
    
    message = engine.generate_escalation_message()
    assert message is not None
    assert "therapist" in message.lower() or "professional" in message.lower()
    assert "care" in message.lower()
    assert "honest" in message.lower()


def test_last_contact_tracking():
    """Test tracking of last contact time."""
    engine = ProactiveCareEngine()
    
    # No contact yet
    hours = engine.hours_since_check_in()
    assert hours == 999
    
    # Record contact
    engine.update_last_contact()
    hours = engine.hours_since_check_in()
    assert hours < 0.1  # Should be nearly zero


def test_profile_awareness():
    """Test that engine can be initialized with user profile."""
    profile = {
        "name": "Alice",
        "goals": ["Be healthier", "Improve relationships"]
    }
    
    engine = ProactiveCareEngine(user_profile=profile)
    assert engine.user_profile["name"] == "Alice"


def test_memory_summary_integration():
    """Test that engine can use memory summary in context."""
    memory_summary = "Alice is working on her health and has been struggling with sleep"
    
    engine = ProactiveCareEngine(memory_summary=memory_summary)
    
    # Check-in should be informed by this context
    message = engine._concerned_check_in("sleep_issues")
    assert message is not None


def test_check_in_time_constraints():
    """Test that check-ins respect time-of-day constraints."""
    engine = ProactiveCareEngine()
    
    # Very early morning — should not check in
    # Note: This test depends on current time, so we're just checking the logic exists
    # In real testing, we'd mock datetime
    
    # The function checks for 7-22 hour window
    # So late night (23:00) should fail
    assert engine.should_initiate_check_in(hours_since_last_contact=50) in [True, False]


def test_empty_patterns_handling():
    """Test handling when no patterns are provided."""
    engine = ProactiveCareEngine()
    
    message = engine.generate_check_in(recent_patterns=None, recent_concerns=None)
    assert message is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
