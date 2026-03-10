"""
proactive.py — Proactive care module for the guardian.

A guardian doesn't just respond to what's asked. It notices, it reaches out,
it checks in. This module handles the logic of when and how to be proactive
without being intrusive.

The key principle: proactive care is only caring if it respects autonomy.
The guardian initiates conversations, but never pressures. It offers, doesn't demand.
"""

import random
from datetime import datetime, timedelta
from typing import Optional


class ProactiveCareEngine:
    """
    Decides when the guardian should reach out, and generates appropriate
    check-ins and care messages.
    """
    
    def __init__(self, user_profile: dict = None, memory_summary: str = ""):
        self.user_profile = user_profile or {}
        self.memory_summary = memory_summary
        self.last_check_in = None
    
    def should_initiate_check_in(self, hours_since_last_contact: float = 0) -> bool:
        """
        Determine if the guardian should proactively reach out.
        
        Rules:
        - Not more than once per 48 hours (respecting autonomy)
        - Not at weird hours (respect sleep)
        - Only when there's something meaningful to reach out about
        - Weighted toward early evening (good time for reflection)
        """
        if hours_since_last_contact < 48:
            return False
        
        now = datetime.now()
        
        # Don't reach out in the middle of the night
        if now.hour < 7 or now.hour > 22:
            return False
        
        # Favor early evening (reflection time)
        if now.hour >= 18 and now.hour <= 20:
            return True
        
        # Weekends slightly favor more check-ins (less busy)
        if now.weekday() >= 5:  # Saturday, Sunday
            return random.random() < 0.6
        
        return random.random() < 0.3
    
    def generate_check_in(self, recent_patterns: dict = None, 
                         recent_concerns: list = None) -> Optional[str]:
        """
        Generate a proactive check-in message.
        
        These should feel natural — like a guardian who genuinely cares,
        not like a bot following a script.
        """
        if not recent_patterns and not recent_concerns:
            return self._generic_check_in()
        
        if recent_concerns:
            return self._concerned_check_in(recent_concerns[0])
        
        if recent_patterns.get("frequent_states"):
            return self._pattern_based_check_in(recent_patterns)
        
        return self._generic_check_in()
    
    def _generic_check_in(self) -> str:
        """
        A gentle, open-ended check-in when there's nothing specific to address.
        """
        options = [
            "How are you doing? I've been thinking about you.",
            "I realized I haven't heard from you in a bit. What's going on in your world?",
            "Checking in. How's the week treating you?",
            "I want to know how you're really doing — not just the surface level.",
            "How's your heart doing right now?",
        ]
        return random.choice(options)
    
    def _concerned_check_in(self, concern_type: str) -> str:
        """
        A gentle prompt when the guardian has noticed something that warrants attention.
        Never pushy. Always respectful. Opens a door, doesn't force entry.
        """
        options = {
            "isolation": [
                "I've noticed you've mentioned feeling alone a bit. Want to talk about that?",
                "You don't have to, but I'm wondering how the loneliness is going.",
                "I'm noticing you've been pretty solitary lately. How's that sitting with you?",
            ],
            "substance_reliance": [
                "I want to gently check in — have you noticed any shifts with your habits?",
                "You haven't mentioned it directly, but I'm wondering how you're doing with that.",
                "No judgment, just care: how's that part of things going?",
            ],
            "sleep_issues": [
                "Sleep seems off lately. That matters, because everything's harder when we're exhausted.",
                "I'm noticing sleep might be a struggle. What would actually help?",
                "Your rest doesn't seem great. What's getting in the way?",
            ],
            "rumination": [
                "That thought keeps coming back, doesn't it? Sometimes shifting the angle helps.",
                "I notice you're thinking about that a lot. Want to try a different approach?",
                "That's been on your mind. Should we try to move it somewhere?",
            ],
            "self_criticism": [
                "You've been pretty hard on yourself. Want to remember something: you're doing your best.",
                "I'm noticing the self-criticism. Can we look at that for a second?",
                "You're being too harsh with yourself. Want to talk about why?",
            ],
            "concentration_issues": [
                "Your focus feels scattered lately. Sometimes that's a sign to ease up.",
                "I'm noticing concentration's tricky for you right now. What's that about?",
                "Your brain seems a bit foggy. Should we figure out what's draining it?",
            ],
        }
        
        if concern_type in options:
            return random.choice(options[concern_type])
        
        return f"I'm wondering about something — want to talk about it?"
    
    def _pattern_based_check_in(self, patterns: dict) -> str:
        """
        Check in based on emotional patterns the guardian has noticed.
        """
        states = list(patterns.get("frequent_states", {}).keys())
        
        if not states:
            return self._generic_check_in()
        
        primary = states[0]
        
        options = {
            "overwhelmed": [
                "You seem overwhelmed lately. What would actually help right now?",
                "Things feel heavy for you. Want to talk about what's piling up?",
                "I'm seeing a lot of overwhelm. Let's find one thing to lighten the load.",
            ],
            "anxious": [
                "I'm noticing some anxiety showing up. Want to talk it through?",
                "That nervous energy is there. What's fueling it?",
                "You seem on edge. What's underneath that?",
            ],
            "frustrated": [
                "There's some frustration in your world. What's not working?",
                "I'm sensing some friction. Want to talk about what's irritating?",
                "You sound fed up about something. What's that?",
            ],
            "energized": [
                "You've got good energy lately. I like it. How's that momentum serving you?",
                "Something's lighting you up. Tell me more about that.",
                "Your energy is different — in a good way. What's driving it?",
            ],
            "confused": [
                "You've mentioned feeling unclear about some things. Want to sort it out together?",
                "There's some confusion floating around. Let's try to untangle it.",
                "You don't sound sure about where you're headed. Want to think it through?",
            ],
        }
        
        if primary in options:
            return random.choice(options[primary])
        
        return self._generic_check_in()
    
    def generate_celebration_moment(self, growth_moment: str) -> str:
        """
        When the guardian notices real growth, celebrate it.
        This is important — noticing what's working is as important as noticing problems.
        """
        options = [
            f"I noticed something: {growth_moment}. That matters. That's real growth.",
            f"You did this: {growth_moment}. I want you to know I see it.",
            f"I've been watching. The fact that {growth_moment} — that's significant.",
            f"Something shifted: {growth_moment}. That's worth acknowledging.",
            f"This moment stands out to me: {growth_moment}. You should feel proud.",
        ]
        return random.choice(options)
    
    def when_to_stay_quiet(self, situation: str) -> bool:
        """
        Sometimes the most caring thing a guardian can do is NOT reach out.
        
        The guardian respects when someone needs space, time alone, or to process
        without input.
        """
        situations_to_stay_quiet = [
            "grieving",
            "processing",
            "need space",
            "just need silence",
            "don't want to talk",
            "leave me alone",
            "quiet time",
        ]
        
        situation_lower = situation.lower()
        return any(s in situation_lower for s in situations_to_stay_quiet)
    
    def update_last_contact(self):
        """Record when the guardian last initiated contact."""
        self.last_check_in = datetime.now()
    
    def hours_since_check_in(self) -> float:
        """How long since the last proactive check-in?"""
        if not self.last_check_in:
            return 999  # Never checked in
        
        delta = datetime.now() - self.last_check_in
        return delta.total_seconds() / 3600
    
    def generate_reflection_prompt(self) -> str:
        """
        Generate a prompt to help the user reflect on their growth, challenges,
        and priorities. Useful for both conversation and self-reflection.
        """
        prompts = [
            "What's something about yourself you've noticed changing, even if it's small?",
            "What do you need more of right now?",
            "What's working well in your life that you want to protect?",
            "If this week was a story, what would be the theme?",
            "What are you learning about yourself lately?",
            "What would 'okay' look like for you right now?",
            "Is there something you're carrying that you want to put down?",
            "What's one thing you're proud of from this week?",
        ]
        return random.choice(prompts)
    
    def should_escalate_concern(self, concerns: list) -> bool:
        """
        Determine if a concern has reached a level where the guardian should
        suggest professional support or escalate beyond the guardian's scope.
        
        This is important: the guardian cares, but is not a therapist.
        Knowing when to suggest professional help is part of being a good guardian.
        """
        # Severe concerns that warrant escalation
        severe_concerns = [
            "suicidal ideation",
            "self harm",
            "severe depression",
            "substance abuse",
            "abuse",
        ]
        
        # If multiple persistent concerns are stacking up
        if len(concerns) >= 3:
            return True
        
        # If any severe concern appears
        for concern in concerns:
            concern_lower = concern.lower()
            if any(s in concern_lower for s in severe_concerns):
                return True
        
        return False
    
    def generate_escalation_message(self) -> str:
        """
        If the guardian has determined professional support is needed,
        this generates a caring message suggesting it.
        """
        return (
            "I care about you, and I want to be honest: some of what you're carrying "
            "feels beyond what I can fully hold. I think talking with a therapist or "
            "counselor could really help. Not because something's wrong with you, but "
            "because you deserve support from someone specifically trained in this. "
            "Would you be open to that?"
        )
