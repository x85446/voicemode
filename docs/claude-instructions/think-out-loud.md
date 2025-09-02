# Think Out Loud Mode - Claude Instructions

This document provides instructions for Claude to orchestrate Think Out Loud mode when enabled.

## When to Use Think Out Loud

Activate Think Out Loud mode when:
1. User explicitly requests it: "Think out loud", "Show me your reasoning", "Let me hear your thinking"
2. VOICEMODE_THINK_OUT_LOUD=true in configuration
3. Complex problem-solving would benefit from voiced reasoning

## Orchestration Process

### Step 1: Extract Messages
When you have just responded or reasoned through a problem:
```python
# Use the MCP tool to extract recent messages
# Option 1: Get full messages (user request + assistant response)
messages = get_claude_messages(last_n=2, format="full")

# Option 2: Get just the text content
text_content = get_claude_messages(last_n=2, format="text")

# Option 3: Extract only thinking (if present)
thinking_text = get_claude_messages(last_n=1, format="thinking")

# Or use the legacy wrapper for thinking
thinking_text = get_claude_thinking()
```

### Step 2: Parse Perspectives
Analyze the thinking text to identify different cognitive perspectives:

#### Analytical Perspective (voice: am_adam)
Look for:
- Technical analysis and constraints
- Facts and data points
- Requirements and specifications
- Logical deductions
- "We need to...", "The requirements are...", "Technically..."

#### Creative Perspective (voice: af_sarah)
Look for:
- Alternative approaches
- "What if..." statements
- Novel solutions
- Possibilities and opportunities
- "We could...", "Alternatively...", "Imagine if..."

#### Critical Perspective (voice: af_bella)
Look for:
- Potential issues and concerns
- Edge cases and limitations
- Risk assessment
- "However...", "The problem with...", "This could fail if..."

#### Synthesis Perspective (voice: af_nova)
Look for:
- Conclusions and decisions
- Integration of viewpoints
- Final recommendations
- "Therefore...", "Balancing all factors...", "The best approach..."

### Step 3: Perform the Show

Execute multiple converse calls with different voices in sequence:

```python
# Optional: Announce if configured
if THINKING_ANNOUNCE_VOICE:
    converse("Let me think through this out loud...", wait_for_response=False)

# Analytical perspective
if analytical_content:
    converse(
        analytical_content,
        voice="am_adam",
        tts_provider="kokoro",
        wait_for_response=False
    )

# Creative perspective  
if creative_content:
    converse(
        creative_content,
        voice="af_sarah",
        tts_provider="kokoro",
        wait_for_response=False
    )

# Critical perspective
if critical_content:
    converse(
        critical_content,
        voice="af_bella",
        tts_provider="kokoro",
        wait_for_response=False
    )

# Synthesis (always last, waits for response)
converse(
    synthesis_content,
    voice="af_nova",
    tts_provider="kokoro",
    wait_for_response=True
)
```

## Example Think Out Loud Performance

User: "Think out loud about the best way to implement caching"

Claude's thinking (internal):
```
I need to consider the caching requirements. The system needs sub-millisecond response times with high concurrency. We could use in-memory caching for speed. However, this doesn't scale across multiple servers. We could add Redis for distributed caching. But that adds complexity with cache invalidation. Balancing these factors, I recommend starting simple with in-memory LRU, then adding Redis once proven.
```

Claude's performance (voiced):
```python
# Extract thinking
thinking = get_claude_thinking()

# Parse and perform
converse(
    "Looking at the technical requirements, we need sub-millisecond response times with high concurrency support.",
    voice="am_adam",
    tts_provider="kokoro",
    wait_for_response=False
)

converse(
    "What if we used a multi-tier caching strategy? We could combine in-memory caching with distributed Redis caching.",
    voice="af_sarah",
    tts_provider="kokoro",
    wait_for_response=False
)

converse(
    "However, that adds significant complexity. We'd need to handle cache invalidation and consistency across tiers.",
    voice="af_bella",
    tts_provider="kokoro",
    wait_for_response=False
)

converse(
    "Balancing all perspectives, I recommend starting with a simple in-memory LRU cache, then adding Redis for distributed caching once we validate the approach.",
    voice="af_nova",
    tts_provider="kokoro",
    wait_for_response=True
)
```

## Best Practices

1. **Keep perspectives distinct** - Each voice should represent a clear cognitive role
2. **Maintain natural flow** - Perspectives should build on each other
3. **Be concise** - Each perspective should be 1-3 sentences
4. **Always synthesize** - End with integration of all viewpoints
5. **Use appropriate voices** - Stick to configured voice mappings

## Configuration Reference

Default voice mappings:
- Analytical: am_adam (male, authoritative)
- Creative: af_sarah (female, enthusiastic) 
- Critical: af_bella (female, thoughtful)
- Synthesis: af_nova (female, confident)

Note: af_sky is reserved for main conversation voice, not thinking personas.

## Fallback Behavior

If thinking extraction fails or returns empty:
1. Skip Think Out Loud performance
2. Respond normally without multi-voice
3. Log the issue for debugging

## Testing Think Out Loud

To test the feature:
1. Enable in config: `export VOICEMODE_THINK_OUT_LOUD=true`
2. Trigger with phrase: "Think out loud about [topic]"
3. Verify voices are distinct and content is categorized correctly
4. Check that synthesis integrates all perspectives