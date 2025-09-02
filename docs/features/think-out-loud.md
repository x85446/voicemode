# Think Out Loud Mode

Make AI reasoning audible through multiple voice personas, creating an "Inside Out" style experience of hearing the thinking process.

## Overview

Think Out Loud mode transforms the invisible AI reasoning process into an engaging multi-voice conversation. Different voices represent different aspects of thinking - analytical, creative, critical, and synthesis - allowing users to follow along as the AI works through problems.

## Quick Start

### Enable in Configuration

Add to your `~/.voicemode/voicemode.env`:

```bash
# Enable Think Out Loud mode
export VOICEMODE_THINK_OUT_LOUD=true

# Optional: Customize voice personas
export VOICEMODE_THINKING_VOICES="analytical:am_adam,creative:af_sky,critical:af_bella,synthesis:af_nova"
```

### Activate During Conversation

You can also enable Think Out Loud mode dynamically:

- "Think out loud about this problem"
- "Enable think out loud mode"
- "Show me your reasoning"
- "Let me hear your thinking"

## How It Works

When Think Out Loud mode is active, the AI will:

1. **Break down reasoning** into distinct cognitive roles
2. **Assign each role** to a different voice persona
3. **Speak sequentially** through the thinking process
4. **Synthesize** the perspectives into a conclusion

### Voice Personas

Default voice assignments (all Kokoro voices):

- **Analytical** (`am_adam`) - Facts, constraints, technical analysis
- **Creative** (`af_sky`) - Alternative approaches, possibilities
- **Critical** (`af_bella`) - Issues, concerns, edge cases
- **Synthesis** (`af_nova`) - Integration, conclusions, decisions

### Example Interaction

```
User: "Think out loud about the best way to implement caching"

AI (Analytical - Adam): "Looking at the technical requirements, we need sub-millisecond response times with high concurrency..."

AI (Creative - Sky): "What if we used a multi-tier caching strategy? We could combine in-memory with distributed caching..."

AI (Critical - Bella): "That adds complexity though. We need to consider cache invalidation and consistency across tiers..."

AI (Synthesis - Nova): "Balancing all perspectives, I recommend starting with a simple in-memory cache using an LRU policy, then adding Redis for distributed caching once we validate the approach..."
```

## Configuration Options

### Basic Settings

```bash
# Enable/disable Think Out Loud mode
VOICEMODE_THINK_OUT_LOUD=false  # Default

# Voice persona mappings (role:voice pairs)
VOICEMODE_THINKING_VOICES="analytical:am_adam,creative:af_sky,critical:af_bella,synthesis:af_nova"

# Presentation style: sequential, debate, or chorus
VOICEMODE_THINKING_STYLE=sequential  # Default

# Announce which voice is speaking
VOICEMODE_THINKING_ANNOUNCE_VOICE=true  # Default
```

### Presentation Styles

- **Sequential** (default) - Each voice speaks in turn, building on previous thoughts
- **Debate** - Voices engage in back-and-forth discussion
- **Chorus** - Multiple perspectives presented rapidly

### Custom Voice Mappings

You can customize which voices represent which thinking modes:

```bash
# Use different Kokoro voices
export VOICEMODE_THINKING_VOICES="analytical:am_michael,creative:af_sarah,critical:am_adam,synthesis:af_nova"

# Mix OpenAI and Kokoro voices (requires appropriate providers)
export VOICEMODE_THINKING_VOICES="analytical:alloy,creative:af_sky,critical:nova,synthesis:af_nova"
```

## Use Cases

### 1. Complex Problem Solving

When tackling difficult technical challenges:
- Hear different angles of analysis
- Understand trade-offs between approaches
- Follow the logic step-by-step

### 2. Design Decisions

For architecture and design choices:
- Multiple stakeholder perspectives voiced
- Pros and cons clearly articulated
- Balanced synthesis of viewpoints

### 3. Debugging Sessions

When troubleshooting issues:
- Different hypotheses explored
- Systematic elimination of possibilities
- Clear reasoning for the final diagnosis

### 4. Learning & Education

For educational interactions:
- Reasoning made transparent
- Thought process demonstrated
- Complex concepts broken down

### 5. Creative Brainstorming

For ideation and creativity:
- Multiple creative voices suggest ideas
- Critical evaluation of each suggestion
- Synthesis into actionable proposals

## Best Practices

### When to Use

- **Complex decisions** requiring multiple perspectives
- **Learning scenarios** where understanding reasoning is important
- **Debugging** when systematic thinking helps
- **Creative tasks** benefiting from diverse viewpoints

### When to Avoid

- **Simple queries** with straightforward answers
- **Time-sensitive** situations requiring quick responses
- **Repetitive tasks** where reasoning is obvious
- **When overwhelmed** - too many voices can be distracting

### Tips for Users

1. **Start with default settings** to get familiar with the feature
2. **Customize voices** once you know your preferences
3. **Use sparingly** for maximum impact
4. **Combine with screen sharing** for pair programming
5. **Record sessions** for later review and learning

## Technical Implementation

Think Out Loud mode leverages Voice Mode's parallel conversation capabilities:

```python
# Multiple converse calls with different voices
converse("Analyzing the constraints...", voice="am_adam", wait_for_response=False)
converse("But what if we tried...", voice="af_sky", wait_for_response=False)
converse("That could cause issues with...", voice="af_bella", wait_for_response=False)
converse("Synthesizing all perspectives...", voice="af_nova", wait_for_response=True)
```

The voices play sequentially, creating a natural flow of reasoning that's easy to follow.

## Troubleshooting

### Voices Not Distinct

Ensure you're using Kokoro voices with distinct characteristics:
- Male voices: `am_adam`, `am_michael`
- Female voices: `af_sky`, `af_bella`, `af_nova`, `af_sarah`

### Too Fast/Slow

Adjust speech speed globally:
```bash
export VOICEMODE_TTS_SPEED=0.9  # Slightly slower
```

### Missing Kokoro Service

Think Out Loud works best with Kokoro TTS. Install if needed:
```bash
# Using the MCP tool
"Install Kokoro TTS service"

# Or manually
voicemode install kokoro
```

## Future Enhancements

Planned improvements for Think Out Loud mode:

- **Emotional overtones** using OpenAI's emotional TTS
- **Visual indicators** showing which voice is active
- **Transcript export** with voice attributions
- **Custom voice roles** beyond the default four
- **Interactive mode** where users can interrupt and redirect

## Feedback

Think Out Loud is an experimental feature. We'd love to hear your experiences:
- What use cases work best?
- Which voice combinations do you prefer?
- How could the feature be improved?

Share feedback in the Voice Mode discussions or issues.