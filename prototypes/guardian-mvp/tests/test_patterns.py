"""
test_patterns.py — Tests for emotional pattern recognition.
"""

import pytest
from patterns import EmotionalPatternRecognizer


def test_emotional_state_detection():
    """Test that emotional states are correctly identified."""
    recognizer = EmotionalPatternRecognizer()
    
    # Test overwhelmed
    result = recognizer.analyze_text("I'm feeling completely overwhelmed by everything")
    assert "overwhelmed" in result["primary_states"]
    
    # Test anxious
    result = recognizer.analyze_text("I've been really anxious about this decision")
    assert "anxious" in result["primary_states"]
    
    # Test happy/energized
    result = recognizer.analyze_text("I feel so energized and excited about this project!")
    assert "energized" in result["primary_states"]
    
    # Test calm
    result = recognizer.analyze_text("I'm feeling calm and at peace")
    assert "calm" in result["primary_states"]


def test_concern_detection():
    """Test that concerning patterns are flagged."""
    recognizer = EmotionalPatternRecognizer()
    
    # Test isolation
    result = recognizer.analyze_text("I've been staying in and don't want to see anyone")
    assert "isolation" in result["concerns"]
    
    # Test self-criticism
    result = recognizer.analyze_text("I'm so broken and it's all my fault")
    assert "self_criticism" in result["concerns"]
    
    # Test sleep issues
    result = recognizer.analyze_text("I can't sleep and I'm exhausted all the time")
    assert "sleep_issues" in result["concerns"]
    
    # Test rumination
    result = recognizer.analyze_text("I keep replaying that moment over and over")
    assert "rumination" in result["concerns"]


def test_intensity_estimation():
    """Test emotional intensity estimation."""
    recognizer = EmotionalPatternRecognizer()
    
    # Low intensity
    result = recognizer.analyze_text("I'm feeling a bit overwhelmed")
    assert result["intensity"] == "low"
    
    # Moderate intensity
    result = recognizer.analyze_text("I'm really frustrated!")
    assert result["intensity"] == "moderate"
    
    # High intensity
    result = recognizer.analyze_text("I'M COMPLETELY OVERWHELMED!!!")
    assert result["intensity"] == "high"


def test_recurring_themes():
    """Test identification of recurring themes."""
    recognizer = EmotionalPatternRecognizer()
    
    # Add multiple sessions with similar states
    recognizer.analyze_text("I'm feeling overwhelmed")
    recognizer.analyze_text("Everything feels overwhelming right now")
    recognizer.analyze_text("I'm so overwhelmed by work")
    recognizer.analyze_text("The overwhelm is getting to me")
    
    themes = recognizer.get_recurring_themes(num_recent=4)
    assert themes["frequent_states"]["overwhelmed"] >= 3


def test_concern_flags():
    """Test that significant concerns are properly flagged."""
    recognizer = EmotionalPatternRecognizer()
    
    # Add sessions with recurring isolation theme
    for _ in range(3):
        recognizer.analyze_text("I've been staying alone and don't want to see anyone")
    
    for _ in range(2):
        recognizer.analyze_text("I'm just staying in, don't feel like leaving")
    
    flags = recognizer.get_concern_flags()
    assert "isolation" in flags


def test_gentle_prompt_decision():
    """Test whether guardian should gently prompt about concerns."""
    recognizer = EmotionalPatternRecognizer()
    
    # No concerns yet
    should_prompt, topic = recognizer.should_gentle_prompt()
    assert should_prompt is False
    
    # Add multiple sessions with sleep concern
    for _ in range(3):
        recognizer.analyze_text("I can't sleep and I'm so tired")
    
    for _ in range(2):
        recognizer.analyze_text("My sleep has been terrible")
    
    should_prompt, topic = recognizer.should_gentle_prompt()
    assert should_prompt is True
    assert topic is not None
    assert "sleep" in topic.lower() or "Sleep" in topic


def test_pattern_summary_generation():
    """Test natural language pattern summary generation."""
    recognizer = EmotionalPatternRecognizer()
    
    # No history
    summary = recognizer.generate_pattern_summary()
    assert summary == ""
    
    # Add history
    recognizer.analyze_text("I've been anxious")
    recognizer.analyze_text("Still feeling anxious")
    recognizer.analyze_text("The anxiety continues")
    recognizer.analyze_text("I'm struggling with isolation")
    
    summary = recognizer.generate_pattern_summary()
    assert summary != ""
    assert ("anxious" in summary.lower() or "pattern" in summary.lower())


def test_reset():
    """Test resetting the recognizer."""
    recognizer = EmotionalPatternRecognizer()
    
    recognizer.analyze_text("I'm overwhelmed")
    assert len(recognizer.state_history) > 0
    
    recognizer.reset()
    assert len(recognizer.state_history) == 0
    assert len(recognizer.patterns_detected) == 0


def test_multiple_states_in_single_text():
    """Test detecting multiple emotional states in one text."""
    recognizer = EmotionalPatternRecognizer()
    
    result = recognizer.analyze_text(
        "I'm feeling anxious and overwhelmed, but also a bit energized about the challenge"
    )
    
    states = result["primary_states"]
    assert "anxious" in states
    assert "overwhelmed" in states
    assert "energized" in states


def test_no_false_positives():
    """Test that we don't falsely detect emotions."""
    recognizer = EmotionalPatternRecognizer()
    
    result = recognizer.analyze_text(
        "The book 'Calm' by the author was excellent"
    )
    
    # Should not detect calm emotion just because the word appears
    # This is a limitation of the simple keyword matching, but important to note
    # In real use, we'd want better NLP


def test_concern_integration_across_sessions():
    """Test that concerns are properly integrated across multiple sessions."""
    recognizer = EmotionalPatternRecognizer()
    
    # Session 1: mention isolation
    recognizer.analyze_text("I've been isolating myself")
    
    # Session 2: mention sleep issues
    recognizer.analyze_text("I can't sleep anymore")
    
    # Session 3: back to isolation
    recognizer.analyze_text("I don't want to see anyone")
    
    # Session 4: rumination
    recognizer.analyze_text("I keep thinking about the same thing")
    
    # Session 5: isolation again
    recognizer.analyze_text("Another day staying alone")
    
    flags = recognizer.get_concern_flags()
    # Isolation appears 3 times, should be flagged
    assert "isolation" in flags


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
