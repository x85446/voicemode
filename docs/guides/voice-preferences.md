# Voice Preferences Configuration

Voice Mode supports project-local and hierarchical voice preferences through `.voices.txt` files. This allows you to configure preferred TTS voices for specific projects, teams, or your entire organization.

## Quick Start

Create a `.voices.txt` file in your project directory:

```
nova
shimmer
alloy
```

Voice Mode will use these voices in preference order when speaking in this project.

## File Locations

Voice Mode searches for `.voices.txt` files in the following order:

1. **Current directory** - `.voices.txt`
2. **Parent directories** - walks up the directory tree checking each parent
3. **Voicemode subdirectory** - `.voicemode/voices.txt` in current or parent dirs
4. **User home** - `~/.voices.txt`
5. **User voicemode config** - `~/.voicemode/voices.txt`

The first file found is used. This allows flexible configuration at different levels.

## File Format

The `.voices.txt` file format is simple:
- One voice name per line
- Lines starting with `#` are comments
- Empty lines are ignored
- Voice names are used in the order listed

Example:
```
# Project voice preferences
nova        # Primary voice
shimmer     # Fallback voice
alloy       # Third preference

# Additional voices for testing
echo
fable
```

## Hierarchical Configuration

You can organize voice preferences at different levels of your directory structure:

```
~/work/                           # Organization root
  .voices.txt                     # Company-wide defaults
  
  team-alpha/                     # Team directory
    .voices.txt                   # Team preferences
    
    project-1/                    # Project directory
      .voices.txt                 # Project-specific voices
      src/
      tests/
```

When working in `project-1`, Voice Mode will find and use `project-1/.voices.txt`. If that doesn't exist, it checks `team-alpha/.voices.txt`, then `~/work/.voices.txt`.

## Available Voices

### OpenAI Voices
- `nova` - Natural, friendly voice
- `shimmer` - Warm, inviting voice  
- `alloy` - Neutral, balanced voice
- `echo` - Smooth, calm voice
- `fable` - Expressive, dynamic voice
- `onyx` - Deep, authoritative voice

### Kokoro Voices (Local TTS)
Kokoro provides multilingual voices with different accents and styles:

**English Voices:**
- `af_bella`, `af_nicole`, `af_sarah`, `af_sky` - American female
- `am_adam`, `am_michael` - American male
- `bf_emma`, `bf_isabella` - British female
- `bm_george`, `bm_lewis` - British male

**Other Languages:**
- Spanish: `ef_dora` (female), `em_alex` (male)
- French: `ff_siwis` (female)
- Italian: `if_sara` (female), `im_nicola` (male)
- Portuguese: `pf_dora` (female), `pm_alex` (male)
- Chinese: `zf_xiaobei` (female), `zm_yunjian` (male)
- Japanese: `jf_alpha` (female), `jm_kumo` (male)
- Hindi: `hf_alpha` (female), `hm_omega` (male)

## Use Cases

### Personal Preference
Set your preferred voice globally in `~/.voices.txt`:
```
nova
```

### Project-Specific Voices
Use specific voices for different projects:

**Gaming Project** (`.voices.txt`):
```
fable    # Expressive for game narration
echo     # Calm for instructions
```

**Documentation Project** (`.voices.txt`):
```
alloy    # Clear and neutral
nova     # Friendly alternative
```

### Team Standards
Standardize voices across your team by placing `.voices.txt` in a shared parent directory:
```
# Team voice standard
shimmer   # Primary team voice
nova      # Approved alternative
```

### Multilingual Projects
Configure language-appropriate voices:
```
# International project voices
ef_dora     # Spanish content
ff_siwis    # French content  
zf_xiaobei  # Chinese content
nova        # English fallback
```

## How It Works

1. When Voice Mode starts a conversation, it calls `get_preferred_voices()`
2. The system searches for `.voices.txt` starting from the current directory
3. It walks up the directory tree until finding a file or reaching the filesystem root
4. The preferences are cached for the session to avoid repeated file reads
5. Voice selection uses these preferences when choosing which TTS voice to use

## Tips

- **Version Control**: Consider adding `.voices.txt` to `.gitignore` if voice preferences are personal
- **Documentation**: Add a comment in your `.voices.txt` explaining voice choices
- **Testing**: Use project-specific voices to test how your application sounds with different TTS options
- **Consistency**: Use parent directory configs to maintain consistent voice branding across related projects

## Troubleshooting

If voices aren't being applied:
1. Check that `.voices.txt` is in the correct location
2. Verify voice names are spelled correctly
3. Ensure the file has proper line endings (LF or CRLF)
4. Check file permissions are readable
5. Look for Voice Mode logs mentioning "Found voice preferences at:"

## Example Configurations

### Solo Developer
```
# ~/.voices.txt
nova      # My favorite voice
shimmer   # Good alternative
```

### Open Source Project
```
# project/.voices.txt  
# Standard voices for demos and documentation
alloy     # Neutral for tutorials
nova      # Friendly for examples
echo      # Calm for error messages
```

### Corporate Environment
```
# /company/products/.voices.txt
# Approved voices for customer-facing content
shimmer   # Brand voice
nova      # Alternative brand voice
# Do not use other voices without approval
```