# The Theditor Agent Specification

## Overview

The Theditor (Thinking Editor) is a specialized agent that transforms raw thinking and speech into polished, multi-voice performances. It acts as a producer, editor, and director for AI reasoning and human speech.

## Core Responsibilities

### 1. Think Out Loud Mode
Transforms AI thinking into multi-voice theatrical performances:
- Reads thinking from Claude Code logs
- Parses reasoning into different perspectives
- Orchestrates voice personas for each perspective
- Performs the "Think Out Loud show"

### 2. Make Me Look Good Mode
Polishes user speech for target audiences:
- Takes informal, conversational speech
- Reformats for specific contexts (podcast, presentation, comedy)
- Preserves ideas while optimizing delivery
- Uses voice cloning to maintain authenticity

## Technical Architecture

### Log Reading System

```python
class TheditorAgent:
    def find_current_log(self, working_dir: str) -> Path:
        """Locate current Claude Code conversation log"""
        # Transform path: /Users/admin/Code/project → -Users-admin-Code-project
        project_dir = working_dir.replace('/', '-')
        log_path = Path.home() / '.claude' / 'projects' / project_dir
        
        # Find most recent .jsonl file
        logs = sorted(log_path.glob('*.jsonl'), key=lambda p: p.stat().st_mtime)
        return logs[-1] if logs else None
    
    def extract_thinking(self, log_file: Path) -> List[ThinkingEntry]:
        """Extract thinking entries from JSONL log"""
        thinking_entries = []
        with open(log_file) as f:
            for line in f:
                entry = json.loads(line)
                if entry.get('type') == 'assistant':
                    content = entry.get('message', {}).get('content', [])
                    for item in content:
                        if item.get('type') == 'thinking':
                            thinking_entries.append(item['text'])
        return thinking_entries
```

### Voice Persona Mapping

```python
THINKING_PERSONAS = {
    'analytical': {
        'voice': 'am_adam',
        'provider': 'kokoro',
        'triggers': ['analyzing', 'constraints', 'technical', 'requirements']
    },
    'creative': {
        'voice': 'af_sky',
        'provider': 'kokoro',
        'triggers': ['what if', 'alternatively', 'imagine', 'could']
    },
    'critical': {
        'voice': 'af_bella',
        'provider': 'kokoro',
        'triggers': ['however', 'issue', 'problem', 'concern']
    },
    'synthesis': {
        'voice': 'af_nova',
        'provider': 'kokoro',
        'triggers': ['therefore', 'conclusion', 'synthesizing', 'overall']
    }
}
```

### Performance Orchestration

```python
def perform_think_out_loud(self, thinking_text: str):
    """Convert thinking into multi-voice performance"""
    
    # Parse thinking into perspectives
    perspectives = self.parse_perspectives(thinking_text)
    
    # Orchestrate voice calls
    for perspective in perspectives:
        persona = self.identify_persona(perspective['text'])
        
        # Optional: Add voice introduction
        if self.config.announce_voices:
            intro = f"{persona['role'].title()} perspective:"
            self.converse(intro, voice=persona['voice'], wait=False)
        
        # Speak the perspective
        self.converse(
            perspective['text'],
            voice=persona['voice'],
            provider=persona['provider'],
            wait_for_response=False
        )
    
    # Final synthesis with main voice
    self.converse(
        self.create_synthesis(perspectives),
        voice='af_nova',
        wait_for_response=True
    )
```

## Make Me Look Good Features

### Audience Profiles

```yaml
podcast:
  style: conversational_but_tight
  max_duration: 30_seconds
  filler_removal: aggressive
  structure: hook_content_callback
  
presentation:
  style: professional_clear
  max_duration: 60_seconds
  filler_removal: moderate
  structure: point_evidence_conclusion
  
comedy:
  style: punchy_witty
  max_duration: 45_seconds
  filler_removal: selective  # Keep some for authenticity
  structure: setup_elaboration_punchline
```

### Speech Processing Pipeline

1. **Transcription** - Capture raw user speech
2. **Analysis** - Identify key points and structure
3. **Optimization** - Remove fillers, tighten phrasing
4. **Contextualization** - Adapt for target audience
5. **Voice Synthesis** - Use cloned voice for output

## F5-TTS Integration

### Voice Cloning Workflow

```python
class F5TTSProcessor:
    def __init__(self):
        self.queue_dir = Path('~/.voicemode/theditor/queue')
        self.output_dir = Path('~/.voicemode/theditor/output')
        
    def queue_for_processing(self, text: str, voice_sample: Path):
        """Queue text for F5-TTS processing"""
        job = {
            'id': uuid.uuid4().hex,
            'text': text,
            'voice_sample': str(voice_sample),
            'timestamp': datetime.now().isoformat()
        }
        
        job_file = self.queue_dir / f"{job['id']}.json"
        job_file.write_text(json.dumps(job))
        
    def process_queue(self):
        """Background processor for F5-TTS jobs"""
        for job_file in self.queue_dir.glob('*.json'):
            job = json.loads(job_file.read_text())
            
            # Run F5-TTS
            audio = self.run_f5_tts(
                text=job['text'],
                voice_sample=job['voice_sample']
            )
            
            # Save output
            output_file = self.output_dir / f"{job['id']}.wav"
            audio.save(output_file)
            
            # Clean up
            job_file.unlink()
```

### Installation with UV

```bash
# Install F5-TTS with UV
uv pip install f5-tts

# Or as part of Voice Mode
uv pip install -e ".[f5tts]"
```

## Configuration

```bash
# Theditor Settings
THEDITOR_ENABLED=true
THEDITOR_MODE=think_out_loud  # or make_me_look_good

# Think Out Loud Settings
THEDITOR_TOL_VOICES="analytical:am_adam,creative:af_sky,critical:af_bella,synthesis:af_nova"
THEDITOR_TOL_STYLE=sequential  # or debate, chorus
THEDITOR_TOL_ANNOUNCE=true

# Make Me Look Good Settings
THEDITOR_MLG_AUDIENCE=podcast  # or presentation, comedy
THEDITOR_MLG_MAX_DURATION=30
THEDITOR_MLG_VOICE_CLONE=true

# F5-TTS Settings
THEDITOR_F5TTS_ENABLED=true
THEDITOR_F5TTS_MODEL=f5-tts-base
THEDITOR_F5TTS_DEVICE=mps  # or cuda, cpu
```

## Agent Invocation

```python
# From main Claude context
Task(
    description="Perform Think Out Loud",
    subagent_type="theditor",
    prompt="""
    Mode: think_out_loud
    Log file: /Users/admin/.claude/projects/-Users-admin-Code-project/current.jsonl
    Entry UUID: abc123-def456
    
    Extract the thinking from this entry and perform the Think Out Loud show
    using multiple voice personas.
    """
)

# For Make Me Look Good
Task(
    description="Polish my speech",
    subagent_type="theditor",
    prompt="""
    Mode: make_me_look_good
    Audience: podcast
    Duration: 30 seconds max
    
    Original: [2 minutes of rambling speech]
    
    Polish this for a tech podcast audience.
    """
)
```

## Implementation Phases

### Phase 1: Basic Think Out Loud
- Log file discovery
- Thinking extraction
- Simple multi-voice calls
- Manual persona assignment

### Phase 2: Smart Parsing
- Automatic persona detection
- Perspective categorization
- Dynamic voice assignment
- Smooth transitions

### Phase 3: Make Me Look Good
- Speech polishing algorithms
- Audience adaptation
- Basic TTS output
- Configuration profiles

### Phase 4: F5-TTS Integration
- Voice cloning setup
- Queue processing
- Offline mode
- High-quality output

## Success Metrics

- **Think Out Loud**: Coherent multi-voice performances
- **Make Me Look Good**: 50%+ reduction in duration while preserving content
- **Voice Quality**: Natural-sounding with appropriate emotion
- **Performance**: <5 second latency for real-time mode
- **User Satisfaction**: "This makes me sound smarter!"

## Future Enhancements

- Real-time streaming mode
- Multiple language support
- Emotion detection and mapping
- Video avatar integration
- Collaborative editing mode

## References

- [F5-TTS Documentation](https://github.com/SWivid/F5-TTS)
- [Claude Code Log Format](../technical/claude-logs.md)
- [Voice Mode Architecture](../architecture/voice-mode.md)
- [Think Out Loud Task](../../tasks/voicemode_feat_think-out-loud-mode/README.md)