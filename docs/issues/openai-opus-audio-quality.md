# OpenAI + Opus Audio Quality Issue [RESOLVED]

## Problem Description

~~When using OpenAI TTS with Opus audio format, the audio quality is "absolutely terrible" and "a total mess" according to testing.~~

**UPDATE (2025-06-22)**: This issue has been resolved. Testing confirms that OpenAI now produces good quality audio with Opus format.

## Test Results

### Original Issue (Before Fix)
- **Kokoro + Opus**: Good audio quality ✅
- **OpenAI + Opus**: Terrible audio quality ❌
- **OpenAI + MP3**: Good audio quality ✅

### Current Status (After Fix)
- **Kokoro + Opus**: Good audio quality ✅
- **OpenAI + Opus**: Good audio quality ✅
- **OpenAI + MP3**: Good audio quality ✅

## Environment

- TTS_BASE_URL: Varies (OpenAI API vs local)
- Audio format: Opus (default in new implementation)
- OpenAI TTS model: tts-1
- Voice: nova

## Potential Causes

1. **OpenAI Opus encoding issue**: OpenAI might have a bug in their Opus encoder
2. **Decoding issue**: Our Opus decoding might not handle OpenAI's specific encoding
3. **Format parameters**: OpenAI might use different Opus parameters than expected
4. **API compatibility**: OpenAI's Opus implementation might differ from standard

## Workaround Options

1. **Provider-specific defaults**: Use MP3 for OpenAI, Opus for others
2. **Format detection**: Detect audio quality issues and fall back
3. **User configuration**: Let users override format per provider
4. **Disable Opus for OpenAI**: Remove opus from OpenAI's supported formats

## Recommended Solution

Update the provider configuration to use different default formats:

```python
PROVIDER_DEFAULT_FORMATS = {
    "openai": "mp3",  # Due to Opus quality issues
    "kokoro": "opus",  # Works well with Opus
    "whisper-local": "wav",
    # etc.
}
```

## Testing Needed

1. Test OpenAI with different Opus bitrates
2. Test with different OpenAI models (tts-1-hd)
3. Compare raw Opus files from OpenAI vs Kokoro
4. Test with different audio players to isolate issue