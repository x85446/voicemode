# Frontend URL Configuration Task

## Status: In Progress

## Completed:
- ✅ Added `FRONTEND_URL` environment variable to `voice_mode/config.py`
- ✅ Started importing config in `livekit_frontend_open()` function
- ✅ Added basic logic to use `FRONTEND_URL` if configured

## Still To Do:

### 1. Complete URL handling in frontend.py
- [ ] Update `livekit_frontend_status()` to also respect `FRONTEND_URL`
- [ ] Ensure proper fallback when `FRONTEND_URL` is not set:
  ```python
  # Pseudocode for URL determination logic:
  if config.FRONTEND_URL:
      url = config.FRONTEND_URL
  elif is_ssh_forwarded(port):
      url = f"http://localhost:{port}"
  else:
      url = f"http://{host}:{port}"
  ```

### 2. Handle SSH forwarding edge cases
- [ ] Add logic to detect when user is SSH forwarding on a different port
- [ ] Example: Frontend runs on 3000 locally but forwarded as localhost:3001
- [ ] Implementation approach:
  ```python
  # Check if FRONTEND_URL is set for custom forwarding scenarios
  # This allows: VOICEMODE_FRONTEND_URL=http://localhost:3001
  ```

### 3. Update all URL references
- [ ] Update `livekit_frontend_start()` to show correct URL in output
- [ ] Ensure status messages show the actual accessible URL
- [ ] Update any logging to reflect custom URL when configured

### 4. Add documentation
- [ ] Document `VOICEMODE_FRONTEND_URL` in the main configuration docs
- [ ] Add example use cases:
  - SSH port forwarding on different port
  - Reverse proxy setups (e.g., nginx)
  - Development with custom domains
- [ ] Update README.md configuration section

### 5. Test scenarios
- [ ] Test with no `FRONTEND_URL` set (existing behavior)
- [ ] Test with `FRONTEND_URL=http://localhost:3001` (SSH forwarding)
- [ ] Test with `FRONTEND_URL=https://voice.example.com` (reverse proxy)
- [ ] Test that status and open commands show consistent URLs

## Implementation Notes:
- The `FRONTEND_URL` should be optional and only override automatic detection when set
- When set, it should be used consistently across status, start, and open commands
- The URL should be validated to ensure it's a proper HTTP/HTTPS URL
- Consider adding a warning if `FRONTEND_URL` is set but frontend isn't running