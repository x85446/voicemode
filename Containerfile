# Voice MCP Server Container
FROM python:3.11-slim

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    libsndfile1 \
    ffmpeg \
    pulseaudio-utils \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster Python package management
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy the voice-mcp server script
COPY mcp-servers/voice-mcp /app/voice-mcp

# Make the script executable
RUN chmod +x /app/voice-mcp

# Install Python dependencies using uv
RUN uv pip install --system \
    fastmcp>=2.0.0 \
    sounddevice \
    numpy \
    scipy \
    openai>=1.0.0 \
    python-dotenv \
    livekit-agents>=0.11 \
    livekit-plugins-openai \
    livekit-plugins-silero \
    pydub

# Create recordings directory
RUN mkdir -p /app/recordings

# Environment variables with defaults
ENV STT_BASE_URL=https://api.openai.com/v1
ENV TTS_BASE_URL=https://api.openai.com/v1
ENV TTS_VOICE=nova
ENV TTS_MODEL=tts-1
ENV STT_MODEL=whisper-1
ENV LIVEKIT_URL=ws://localhost:7880
ENV LIVEKIT_API_KEY=devkey
ENV LIVEKIT_API_SECRET=secret
ENV VOICE_MCP_DEBUG=false

# Expose stdio for MCP communication
EXPOSE 8080

# Run the voice-mcp server
CMD ["/app/voice-mcp"]