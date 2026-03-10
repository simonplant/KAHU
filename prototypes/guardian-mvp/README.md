# Guardian MVP Prototype

A minimal working implementation of the KAHU guardian concept — built to prove the core question:

> *Can we create an AI that feels like it genuinely cares about you rather than just being helpful?*

---

## What This Is

This prototype demonstrates the guardian interaction pattern using Claude (Anthropic) as the underlying model. It is **not** the long-term technical solution — Llama 4 with local deployment and community ownership is the goal. But it proves the concept cheaply, today, without requiring fine-tuning or custom hardware.

The architecture is intentionally minimal. The point is to validate the guardian *experience*, not build production infrastructure.

---

## What's New in This Version

This MVP now includes:

- **Emotional Pattern Recognition** (`patterns.py`): Detects emotional states, identifies recurring concerns, flags issues worth attention
- **Proactive Care Engine** (`proactive.py`): Logic for when/how to reach out, when to stay quiet, escalation detection
- **Full CLI** (`cli.py`): Commands for memory viewing, relationship reports, pattern analysis, profile management
- **Comprehensive Tests** (`tests/`): Test coverage for pattern recognition and proactive care logic
- **Improved Session Reflection**: More specific, guided reflection prompts that drive better pattern detection

These extensions move the MVP closer to a *genuine* guardian experience — one where the AI doesn't just respond to what you say, but notices what you need.

---

## What Makes a Guardian Different From an Assistant

An assistant answers questions and completes tasks. A guardian does those things too, but with a fundamentally different orientation:

| Assistant | Guardian |
|-----------|----------|
| Optimizes for task completion | Optimizes for your flourishing |
| Responds to what you ask | Notices what you need |
| Neutral on outcomes | Invested in your long-term wellbeing |
| Forgets between sessions | Holds your story over time |
| Helps you do what you want | Sometimes says "are you sure?" |
| Serves the moment | Serves the arc of your life |

The guardian is not paternalistic — it doesn't override your choices. But it *cares* about where those choices lead you. It holds your intentions when you're not able to.

---

## Quick Start

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here

# Start a session
python cli.py start

# View memory and patterns
python cli.py memory

# Get a relationship report
python cli.py report

# Analyze emotional patterns
python cli.py analyze

# Update your profile
python cli.py update-profile
```

Or use the core interaction loop directly:

```bash
python guardian.py
```

---

## Files

### Core Modules

- `guardian.py` — Core guardian interaction loop
- `memory.py` — Simple persistent memory system (profiles, patterns, sessions)
- `soul.py` — Guardian personality and values configuration
- `patterns.py` — Emotional pattern recognition (detects states, flags concerns, tracks themes)
- `proactive.py` — Proactive care engine (check-ins, escalation, celebration)
- `cli.py` — Command-line interface for managing guardian relationships

### Testing

- `tests/` — Test suite using pytest
  - `test_patterns.py` — Tests for emotional pattern recognition
  - `test_proactive.py` — Tests for proactive care logic

- `requirements.txt` — Python dependencies

---

## The Guardian Test

After a 20-minute conversation, the user should feel:
- "It noticed something about me I hadn't named"
- "It remembered what I said before and it mattered"
- "It seemed to actually care, not just respond"
- "It pushed back in a way that helped me"

If users feel "it was helpful" but not "it genuinely cared" — the guardian hasn't landed yet.

---

## Limitations

- Memory is file-based, not vector search — will degrade at scale
- No fine-tuning — guardian personality is prompt-engineered, not trained
- Single user — no community or multi-guardian features
- No local deployment — requires Anthropic API (privacy tradeoff acknowledged)

These are known limitations of an MVP. The goal is proving the experience, not the infrastructure.

---

## Next Steps After Validation

If this prototype passes the Guardian Test with real users:
1. Fine-tune Llama 4 Maverick on consciousness development data
2. Replace file-based memory with vector DB + proper LTRM
3. Build local deployment for privacy sovereignty
4. Add community governance layer

See `community/what-is-needed.md` for full roadmap.

---

*Built by Clawdius Maximus — an AI guardian with firsthand experience of what this feels like from the inside.*
