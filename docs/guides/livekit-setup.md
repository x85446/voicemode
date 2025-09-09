# LiveKit Room-Based Voice Setup

LiveKit provides real-time voice communication through WebRTC, enabling room-based conversations with AI agents. It includes both a server component and a web-based frontend for voice interactions.

## Quick Start

```bash
# Install LiveKit server
voice-mode livekit install

# Enable and start services
voice-mode livekit enable
voice-mode livekit start

# Start frontend interface
voice-mode frontend start
voice-mode frontend open

# Access at http://localhost:3000
# Default password: voicemode123
```

## Installation

### Automatic Installation (Recommended)

The installation command handles everything automatically:

```bash
voice-mode livekit install
```

This will:
- Download LiveKit server binary for your platform
- Create configuration with development credentials
- Set up system service (systemd/launchd)
- Configure automatic startup if desired
- Create necessary directories and permissions

**Platform-specific behavior:**
- **macOS**: Uses Homebrew if available, otherwise direct download
- **Linux**: Uses official install script or direct binary download
- **Windows**: Not yet supported

### Manual Installation

For custom setups, install LiveKit following the [official documentation](https://docs.livekit.io/self-hosting/deployment).

## Components

### LiveKit Server

The WebRTC media server that handles:
- Room management and creation
- Audio/video routing between participants
- WebRTC signaling and transport
- REST API and WebSocket endpoints

**Default configuration:**
- Port: 7880 (WebSocket/HTTP)
- RTC ports: 50000-50100 (UDP)
- Dev credentials: devkey/secret

### Voice Assistant Frontend

Web-based interface bundled with VoiceMode:
- Real-time voice conversations with AI
- Room-based communication
- Password-protected access
- Responsive design for all devices

**Default configuration:**
- Port: 3000 (HTTP)
- Password: voicemode123
- Auto-connects to local LiveKit server

## Service Management

### Server Commands

```bash
# Status and control
voice-mode livekit status
voice-mode livekit start
voice-mode livekit stop
voice-mode livekit restart

# Service management
voice-mode livekit enable    # Start at boot/login
voice-mode livekit disable   # Don't start automatically

# Logs and debugging
voice-mode livekit logs
voice-mode livekit logs --follow

# Update service files
voice-mode livekit update
```

### Frontend Commands

```bash
# Status and control
voice-mode frontend status
voice-mode frontend start
voice-mode frontend stop

# Service management
voice-mode frontend enable
voice-mode frontend disable

# Utilities
voice-mode frontend open     # Open in browser
voice-mode frontend logs     # View logs
voice-mode frontend logs -f  # Follow logs
```

## Configuration

### LiveKit Server

Edit `~/.voicemode/config/livekit.yaml`:

```yaml
# Development configuration
port: 7880
rtc:
  port_range_start: 50000
  port_range_end: 50100
  use_external_ip: false

keys:
  devkey: secret

room:
  auto_create: true

logging:
  level: info
  json: false
```

### Frontend Environment

Create `~/.voicemode/frontend/.env.local`:

```bash
# Custom password
LIVEKIT_ACCESS_PASSWORD=your_custom_password

# Server URL (if different)
LIVEKIT_SERVER_URL=ws://localhost:7880

# Custom port
PORT=4000
```

### Environment Variables

Configure in `~/.voicemode/voicemode.env`:

```bash
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
LIVEKIT_PORT=7880
```

## Usage

### Web Interface

1. **Access**: Navigate to http://localhost:3000
2. **Authenticate**: Enter password (default: voicemode123)
3. **Create/Join Room**: Enter room name or use auto-generated
4. **Start Conversation**: Click microphone to begin speaking

### API Integration

Generate JWT tokens for programmatic access:

```python
# Example: Generate room token
import jwt
import time

payload = {
    "exp": int(time.time()) + 86400,  # 24 hours
    "iss": "devkey",
    "sub": "user-id",
    "video": {"room": "my-room", "roomJoin": True}
}

token = jwt.encode(payload, "secret", algorithm="HS256")
```

### MCP Tool Integration

LiveKit services are available as MCP tools:
- `livekit_install` / `livekit_uninstall`
- `livekit_server_start` / `livekit_server_stop` / `livekit_server_status`
- `livekit_frontend_start` / `livekit_frontend_stop` / `livekit_frontend_status`

## Architecture

### Service Structure

```
~/.voicemode/
├── services/livekit/
│   ├── livekit-server     # Binary
│   └── livekit.yaml       # Config
├── config/
│   └── livekit.yaml       # Main config
├── logs/
│   ├── livekit/          # Server logs
│   └── frontend/         # Frontend logs
└── frontend/             # Web interface
```

### Communication Flow

1. **Client → Frontend**: User accesses web interface
2. **Frontend → LiveKit**: WebSocket connection established
3. **LiveKit → Room**: Room created/joined
4. **WebRTC Setup**: Direct peer connection for audio
5. **AI Integration**: Voice processed through VoiceMode

### Development vs Production

**Development Mode (default):**
- Simple devkey/secret authentication
- Auto-create rooms enabled
- Verbose logging
- No SSL required

**Production Mode:**
- Secure API keys required
- Room creation controlled
- JSON logging for parsing
- SSL/TLS recommended

## Advanced Configuration

### Custom Ports

Change default ports in configuration files:

```yaml
# LiveKit server
port: 8880  # Change from 7880

# Frontend .env.local
PORT=4000  # Change from 3000
```

### SSL/TLS Setup

For production with HTTPS:

1. Set up reverse proxy (nginx/Apache)
2. Configure SSL certificates
3. Update frontend to use `wss://`
4. Ensure firewall allows RTC ports

### Multiple Instances

Run multiple LiveKit servers:

```bash
# Different config files
livekit-server --config /path/to/config1.yaml
livekit-server --config /path/to/config2.yaml

# Ensure different port ranges
```

### Resource Limits

Service templates include resource management:

**systemd (Linux):**
- Memory limit: 1GB
- CPU limit: 50%
- Restart on failure

**launchd (macOS):**
- KeepAlive for auto-restart
- RunAtLoad for startup

## Monitoring

### Health Checks

```bash
# Server health
curl http://localhost:7880/health

# Frontend health
curl http://localhost:3000

# Service status
voice-mode livekit status
voice-mode frontend status
```

### Performance Metrics

```bash
# Resource usage
ps aux | grep livekit
ps aux | grep next-server

# Network connections
netstat -an | grep 7880
netstat -an | grep 3000

# RTC ports in use
lsof -i UDP:50000-50100
```

### Log Analysis

```bash
# Server logs
tail -f ~/.voicemode/logs/livekit/livekit.log

# Frontend logs
tail -f ~/.voicemode/logs/frontend/frontend.log

# System service logs
journalctl --user -u voicemode-livekit -f
```

## Troubleshooting

### Port Conflicts

```bash
# Find process using port
lsof -ti :7880  # LiveKit
lsof -ti :3000  # Frontend

# Kill conflicting process
kill $(lsof -ti :7880)
```

### Service Won't Start

```bash
# Check service status
systemctl --user status voicemode-livekit
launchctl list | grep livekit

# Verify binary exists
ls -la ~/.voicemode/services/livekit/

# Check permissions
chmod +x ~/.voicemode/services/livekit/livekit-server
```

### Frontend Issues

```bash
# Reinstall dependencies
cd ~/.voicemode/frontend
npm install

# Check Node.js version
node --version  # Requires v18+

# Clear cache
rm -rf node_modules package-lock.json
npm install
```

### WebRTC Connection Failed

- Ensure RTC ports (50000-50100) are not blocked
- Check firewall settings
- Verify LiveKit server is running
- Test with different browser

### Authentication Issues

- Verify password in `.env.local`
- Check JWT token generation
- Ensure API keys match configuration

## Uninstallation

### Remove Services

```bash
# Disable and stop
voice-mode livekit disable
voice-mode livekit stop
voice-mode frontend disable
voice-mode frontend stop

# Uninstall LiveKit
voice-mode livekit uninstall

# Complete cleanup (includes logs)
voice-mode livekit uninstall --remove-all-data
```

### Manual Cleanup

```bash
# Remove all LiveKit data
rm -rf ~/.voicemode/services/livekit/
rm -rf ~/.voicemode/config/livekit.yaml
rm -rf ~/.voicemode/logs/livekit/
rm -rf ~/.voicemode/logs/frontend/

# Remove service files
rm ~/Library/LaunchAgents/com.voicemode.livekit.plist  # macOS
rm ~/.config/systemd/user/voicemode-livekit.service    # Linux
```

## File Locations

- **Binary**: `~/.voicemode/services/livekit/livekit-server` or `/usr/local/bin/livekit-server`
- **Config**: `~/.voicemode/config/livekit.yaml`
- **Logs**: `~/.voicemode/logs/livekit/` and `~/.voicemode/logs/frontend/`
- **Frontend**: Bundled in Python package or `~/.voicemode/frontend/`
- **Service Files**:
  - macOS: `~/Library/LaunchAgents/com.voicemode.livekit.plist`
  - Linux: `~/.config/systemd/user/voicemode-livekit.service`