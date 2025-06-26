# Voice Mode Notebooks

This directory contains Jupyter notebooks for working with voice-mode data.

## conversation_compiler.ipynb

An interactive notebook for compiling and editing voice conversations saved by voice-mode.

### Features

- **Browse Conversations**: View all saved audio files with timestamps and transcriptions
- **Match Conversations**: Automatically pairs TTS and STT files based on timestamps
- **Preview Audio**: Listen to individual conversation segments
- **Compile Audio**: Combine selected segments into a single audio file
- **Export Transcripts**: Generate text transcripts of conversations
- **Session Detection**: Groups conversations by time gaps
- **Audio Analysis**: Analyze audio properties and remove silence

### Usage

1. Install required dependencies:
   ```bash
   pip install gradio pydub scipy numpy pandas jupyter
   ```

2. Launch Jupyter:
   ```bash
   jupyter notebook notebooks/conversation_compiler.ipynb
   ```

3. Run all cells to start the Gradio interface

4. Use the interface to:
   - Browse conversations by date
   - Select segments to compile
   - Preview audio before compiling
   - Export compiled audio and transcripts

### Output

Compiled audio files and transcripts are saved to `~/.voicemode/compilations/`