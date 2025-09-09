# Documentation Reorganization Plan - Simplified

## Target Structure: ~20 files total

```
docs/
├── README.md                    # Documentation index and overview
├── tutorials/
│   ├── getting-started.md      # Quick start guide with first conversation
│   └── development-setup.md    # Setting up for development
├── guides/
│   ├── configuration.md        # All configuration in one place
│   ├── whisper-setup.md        # Setting up Whisper STT service
│   ├── kokoro-setup.md         # Setting up Kokoro TTS service
│   ├── livekit-setup.md        # Setting up LiveKit for room-based voice
│   ├── selecting-voices.md     # Voice selection and preferences
│   ├── troubleshooting.md      # Common issues and solutions
│   └── audio-setup.md          # Microphones, devices, formats
├── reference/
│   ├── api.md                  # API reference
│   ├── cli.md                  # CLI commands and options
│   ├── environment.md          # Environment variables
│   └── mcp-config.md           # MCP configuration format
└── concepts/
    ├── architecture.md         # System architecture overview
    ├── services-overview.md     # How voice services work together
    └── audio-pipeline.md       # Audio processing pipeline
```

## Consolidation Plan

### MERGE these files into `tutorials/getting-started.md`:
- installation-tools.md
- migration-guide.md
- shell-completion.md

### MERGE these files into `tutorials/development-setup.md`:
- local-development-uvx.md
- vscode-configuration.md
- uv.md
- npm-global-no-sudo.md

### MERGE these files into `guides/configuration.md`:
- configuration/configuration-reference.md
- configuration/mcp-env-precedence.md
- configuration/voice-preferences.md
- configuration/voicemode.env.example
- configuration/README.md
- configuration-philosophy.md

### MERGE these files into `guides/whisper-setup.md`:
- services/whisper.md
- services/whisper-coreml.md
- whisper.cpp.md

### MERGE these files into `guides/kokoro-setup.md`:
- services/kokoro.md
- kokoro.md (duplicate)

### MERGE these files into `guides/livekit-setup.md`:
- LIVEKIT_SETUP.md
- livekit-implementation-summary.md
- livekit-service-design.md

### MERGE these files into `concepts/services-overview.md`:
- services/README.md
- install-services-feature.md
- service-health-checks.md

### MERGE these files into `guides/audio-setup.md`:
- audio/devices/README.md
- audio-format-migration.md
- silence-detection.md
- vad-debugging.md

### MERGE these files into `guides/troubleshooting.md`:
- troubleshooting/README.md
- troubleshooting/wsl2-microphone-access.md
- frontend-env-vars-issue.md
- install-robustness-analysis.md

### MERGE these files into `reference/api.md`:
- api-discovery-urls.md
- openai-api-routing.md
- statistics-dashboard.md

### KEEP in `concepts/architecture.md`:
- System architecture and design patterns

### KEEP AS IS:
- guides/selecting-voices.md (already well-focused)
- reference/mcp-config.md (from mcp-config-json.md)
- reference/environment.md (from configuration/mcp-env-precedence.md)

### REMOVE/ARCHIVE:
- yubikey/yubikey-touch-detector.md (not relevant to voicemode)
- web/* (multiple versions of same page - keep only latest index.html)
- gen_pages.py (if using mkdocs, move to build scripts)
- requirements.txt (merge into main project deps)

### SPECIAL FILES:
- Keep `assets/images/` for logos
- Keep one version of web/index.html as project landing page
- Move web/install.sh to project root or scripts/

## Result: 18 documentation files + README + assets

This gives us a clean, navigable structure where:
- Each file has a clear purpose
- No duplicate information
- Easy to find what you need
- Follows standard documentation patterns
- Service-specific guides are separate for clarity