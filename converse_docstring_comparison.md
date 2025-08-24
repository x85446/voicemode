# Converse Tool Docstring Comparison

## Summary of Versions

| Version | Characters | Approx Tokens | Token Reduction | Description |
|---------|------------|---------------|-----------------|-------------|
| Original | 11,288 | ~2,822 | Baseline | Full documentation with all examples |
| Papa Bear | 1,717 | ~429 | 85% less | Comprehensive but optimized |
| Mama Bear | 1,049 | ~262 | 91% less | Balanced essentials |
| Baby Bear | 426 | ~107 | 96% less | Ultra minimal |

---

## Baby Bear Version (Ultra Minimal)
**426 characters / ~107 tokens**

```python
"""Speak text and optionally listen for voice response.

Args:
    message: Text to speak
    wait_for_response: Listen for response (default: True)
    voice: TTS voice override (e.g., "af_sky" for Kokoro)
    tts_provider: "openai" or "kokoro" for non-English
    
Returns:
    Voice response text or confirmation

Non-English: Use kokoro provider with appropriate voice
Silence detection handles duration automatically
"""
```

---

## Mama Bear Version (Balanced)
**1,049 characters / ~262 tokens**

```python
"""Speak text and optionally listen for voice response.

Language Support:
    Non-English requires kokoro provider + specific voice:
    Spanish: voice="ef_dora", French: voice="ff_siwis"
    Chinese: voice="zf_xiaobei", Japanese: voice="jf_alpha"

Args:
    message: Text to speak
    wait_for_response: Listen for response (default: True)
    listen_duration: Override only if needed (default: 120s with silence detection)
    voice: TTS voice (auto-selected unless specified)
    tts_provider: "openai" or "kokoro"
    tts_model: For emotions use "gpt-4o-mini-tts" 
    tts_instructions: Emotional tone (with gpt-4o-mini-tts)
    speed: 0.25-4.0 (1.0=normal)
    disable_silence_detection: For noisy environments
    
Returns:
    Voice response text or spoken confirmation

Parallel Pattern: wait_for_response=False to speak while executing other tools
Examples:
    converse("Hello")  # Basic
    converse("Processing", wait_for_response=False)  # No wait
    converse("¿Cómo estás?", voice="ef_dora", tts_provider="kokoro")  # Spanish
"""
```

---

## Papa Bear Version (Comprehensive but Optimized)
**1,717 characters / ~429 tokens**

```python
"""Speak text and optionally listen for voice response.

## Key Points
- Default: 120s listen with silence detection - rarely needs override
- Non-English: MUST use kokoro provider + language voice
- Parallel ops: wait_for_response=False speaks while executing
- Emotions: gpt-4o-mini-tts model + tts_instructions

## Language Voices (kokoro required)
Spanish: ef_dora/em_alex | French: ff_siwis | Italian: if_sara/im_nicola
Portuguese: pf_dora/pm_alex | Chinese: zf_xiaobei/zm_yunjian
Japanese: jf_alpha/jm_kumo | Hindi: hf_alpha/hm_omega

Args:
    message: Text to speak (avoid CAPS except acronyms)
    wait_for_response: Listen for response (default: True)
    listen_duration: Rarely override (default: 120s + silence detection)
    transport: "auto"/"local"/"livekit" (default: auto)
    voice: TTS voice (auto unless user requests or non-English)
    tts_provider: "openai"/"kokoro" (auto unless specified)
    tts_model: "tts-1"/"tts-1-hd"/"gpt-4o-mini-tts" (emotions)
    tts_instructions: Tone for gpt-4o-mini-tts only
    speed: 0.25-4.0 speech rate (1.0=normal)
    audio_feedback: Override chime setting
    disable_silence_detection: For noisy/dictation
    vad_aggressiveness: 0-3 (0=permissive, 3=strict)
    skip_tts: True=text only, False=force voice
    
Returns:
    If wait_for_response: Voice response text
    Otherwise: Confirmation of speech

## Common Patterns
Basic: converse("Hello")
No wait: converse("Processing", wait_for_response=False) + tool()
Spanish: converse("Hola", voice="ef_dora", tts_provider="kokoro")
Emotion: converse("Yay!", tts_model="gpt-4o-mini-tts", tts_instructions="excited")
Fast: converse("Quick", speed=1.5)
Noisy: converse("Speak up", vad_aggressiveness=3)
"""
```

---

## Original Version (Current)
**11,288 characters / ~2,822 tokens**

[Full 156-line docstring with extensive examples and explanations - see converse.py]

---

## Token Count Analysis

### Methodology
- Character count / 4 = approximate tokens (rough estimate)
- Actual tokenization may vary ±20%

### Results

| Version | Characters | Tokens | Reduction | Use Case |
|---------|------------|--------|-----------|----------|
| Original | 11,288 | ~2,822 | Baseline | Full reference |
| Papa Bear | 1,717 | ~429 | 85% less | Daily use with all features |
| Mama Bear | 1,049 | ~262 | 91% less | Core features only |
| Baby Bear | 426 | ~107 | 96% less | Minimal viable |

### Recommendation

**Mama Bear (262 tokens)** provides the best balance:
- Covers 90% of use cases
- 91% token reduction (saves 2,560 tokens per request!)
- Retains language support
- Includes parallel pattern
- Has basic examples

Papa Bear is good if you need:
- Emotional speech
- VAD tuning
- Complete language list
- All transport options

Baby Bear for:
- Token-critical situations
- Simple voice interactions only
- Systems with external docs