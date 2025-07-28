# Service Health Checks

Voice Mode services now include health check functionality to ensure services are fully ready before reporting as started.

## How It Works

### systemd (Linux)

Services use `ExecStartPost` to check the `/health` endpoint:

```ini
ExecStartPost=/bin/sh -c 'while ! curl -sf http://127.0.0.1:8880/health >/dev/null 2>&1; do echo "Waiting for Kokoro to be ready..."; sleep 1; done; echo "Kokoro is ready!"'
```

Benefits:
- `systemctl start` blocks until service is ready
- Clear status messages during startup
- Immediate feedback on success/failure

### launchd (macOS)

Services use wrapper scripts that perform health checks:

```bash
# Start service and wait for health endpoint
exec "./start-kokoro.sh" &
SERVICE_PID=$!

while ! curl -sf http://127.0.0.1:8880/health >/dev/null 2>&1; do
    if ! kill -0 $SERVICE_PID 2>/dev/null; then
        echo "Service failed to start"
        exit 1
    fi
    echo "Waiting for service to be ready..."
    sleep 1
done
```

## Service Status During Startup

When you check service status during startup, you'll see:

**systemd:**
```
● voicemode-kokoro.service - Voice Mode Kokoro Text-to-Speech Service
     Active: activating (start-post) since Mon 2025-01-28; 3s ago
    Process: 12345 ExecStart=/path/to/start.sh (code=exited, status=0/SUCCESS)
    Process: 12346 ExecStartPost=/bin/sh -c while ! curl... (code=exited, status=0/SUCCESS)
   Main PID: 12345 (python)
     Status: "Waiting for Kokoro to be ready..."
```

**launchd:**
```
Service is starting... (check logs for details)
```

## Endpoints

Both Whisper and Kokoro services provide `/health` endpoints:

- **Whisper**: `http://127.0.0.1:2022/health`
- **Kokoro**: `http://127.0.0.1:8880/health`

These endpoints return 200 OK when the service is ready to handle requests.

## Troubleshooting

If a service fails to become ready:

1. Check service logs:
   - systemd: `journalctl --user -u voicemode-kokoro -f`
   - launchd: `tail -f ~/.voicemode/logs/kokoro/kokoro.log`

2. Manually test the health endpoint:
   ```bash
   curl -v http://127.0.0.1:8880/health
   ```

3. Common issues:
   - Port already in use
   - Model files not found
   - Insufficient memory for model loading