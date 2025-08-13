"""LiveKit Voice Assistant Frontend management."""

import asyncio
import json
import logging
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

from voice_mode.server import mcp

logger = logging.getLogger("voice-mode")


def find_frontend_dir() -> Optional[Path]:
    """Find the voice-assistant-frontend directory."""
    # Check common locations
    voicemode_base = os.path.expanduser(os.environ.get("VOICEMODE_BASE_DIR", "~/.voicemode"))
    
    possible_paths = [
        # Vendor directory (current location)
        Path.home() / "Code" / "github.com" / "mbailey" / "voicemode" / "vendor" / "livekit-voice-assistant" / "voice-assistant-frontend",
        # Potential service directory
        Path(voicemode_base) / "services" / "livekit-frontend",
        # Development location
        Path.home() / "Code" / "voice-assistant-frontend",
    ]
    
    for path in possible_paths:
        if path.exists() and (path / "package.json").exists():
            return path
    
    return None


@mcp.tool()
async def livekit_frontend_start(
    port: int = 3000,
    host: str = "127.0.0.1"
) -> Dict[str, Any]:
    """Start the LiveKit voice assistant frontend.
    
    Starts the Next.js frontend application for voice conversations with LiveKit.
    
    Args:
        port: Port to run the frontend on (default: 3000)
        host: Host to bind to (default: 127.0.0.1)
    
    Returns:
        Dictionary with start status and access URL
    """
    try:
        # Find frontend directory
        frontend_dir = find_frontend_dir()
        if not frontend_dir:
            return {
                "success": False,
                "error": "Voice assistant frontend not found. Please install it first."
            }
        
        # Check if already running
        try:
            result = subprocess.run(
                ["lsof", "-ti", f":{port}"],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                return {
                    "success": False,
                    "error": f"Port {port} is already in use. Frontend may already be running."
                }
        except:
            pass
        
        # Check if dependencies are installed
        node_modules = frontend_dir / "node_modules"
        if not node_modules.exists():
            logger.info("Installing frontend dependencies...")
            subprocess.run(
                ["pnpm", "install"],
                cwd=frontend_dir,
                check=True
            )
        
        # Start the frontend
        env = os.environ.copy()
        env["PORT"] = str(port)
        env["HOST"] = host
        
        process = subprocess.Popen(
            ["pnpm", "dev"],
            cwd=frontend_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment to check if it started
        await asyncio.sleep(3)
        
        if process.poll() is not None:
            # Process exited
            stderr = process.stderr.read().decode() if process.stderr else ""
            return {
                "success": False,
                "error": f"Frontend failed to start: {stderr}"
            }
        
        # Get .env.local settings
        env_file = frontend_dir / ".env.local"
        password = "voicemode123"  # default
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith("LIVEKIT_ACCESS_PASSWORD="):
                        password = line.strip().split("=", 1)[1]
        
        return {
            "success": True,
            "message": f"Frontend started successfully",
            "url": f"http://{host}:{port}",
            "password": password,
            "pid": process.pid,
            "directory": str(frontend_dir)
        }
        
    except Exception as e:
        logger.error(f"Error starting frontend: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
async def livekit_frontend_stop() -> Dict[str, Any]:
    """Stop the LiveKit voice assistant frontend.
    
    Stops any running instance of the voice assistant frontend.
    
    Returns:
        Dictionary with stop status
    """
    try:
        # Find process on port 3000 (default Next.js port)
        result = subprocess.run(
            ["lsof", "-ti", ":3000"],
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            pids = result.stdout.strip().split("\n")
            for pid in pids:
                try:
                    subprocess.run(["kill", "-TERM", pid], check=True)
                except:
                    pass
            
            # Wait a moment
            await asyncio.sleep(2)
            
            # Force kill if still running
            for pid in pids:
                try:
                    subprocess.run(["kill", "-9", pid], check=True)
                except:
                    pass
            
            return {
                "success": True,
                "message": f"Frontend stopped (PIDs: {', '.join(pids)})"
            }
        else:
            return {
                "success": True,
                "message": "Frontend was not running"
            }
            
    except Exception as e:
        logger.error(f"Error stopping frontend: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
async def livekit_frontend_status() -> Dict[str, Any]:
    """Check status of the LiveKit voice assistant frontend.
    
    Returns:
        Dictionary with frontend status and configuration
    """
    try:
        # Check if running
        result = subprocess.run(
            ["lsof", "-ti", ":3000"],
            capture_output=True,
            text=True
        )
        
        is_running = bool(result.stdout.strip())
        pid = result.stdout.strip() if is_running else None
        
        # Find frontend directory
        frontend_dir = find_frontend_dir()
        if not frontend_dir:
            return {
                "running": False,
                "error": "Frontend directory not found"
            }
        
        # Check configuration
        env_file = frontend_dir / ".env.local"
        config = {}
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        # Don't expose secrets
                        if "SECRET" not in key:
                            config[key] = value
        
        return {
            "running": is_running,
            "pid": pid,
            "directory": str(frontend_dir),
            "url": "http://127.0.0.1:3000" if is_running else None,
            "configuration": config
        }
        
    except Exception as e:
        logger.error(f"Error checking frontend status: {e}")
        return {"error": str(e)}


@mcp.tool()
async def livekit_frontend_open() -> Dict[str, Any]:
    """Open the LiveKit voice assistant frontend in the default browser.
    
    Starts the frontend if not already running, then opens it in the browser.
    
    Returns:
        Dictionary with status and URL
    """
    try:
        # Check if frontend is running
        status = await livekit_frontend_status.fn()
        
        if not status.get("running"):
            # Start the frontend first
            logger.info("Frontend not running, starting it first...")
            start_result = await livekit_frontend_start.fn()
            if not start_result.get("success"):
                return {
                    "success": False,
                    "error": f"Failed to start frontend: {start_result.get('error', 'Unknown error')}"
                }
            url = start_result.get("url", "http://127.0.0.1:3000")
            password = start_result.get("password", "Check .env.local")
            
            # Wait a moment for it to fully start
            await asyncio.sleep(3)
        else:
            url = status.get("url", "http://127.0.0.1:3000")
            # Get password from env file
            frontend_dir = find_frontend_dir()
            password = "voicemode123"  # default
            if frontend_dir:
                env_file = frontend_dir / ".env.local"
                if env_file.exists():
                    with open(env_file) as f:
                        for line in f:
                            if line.startswith("LIVEKIT_ACCESS_PASSWORD="):
                                password = line.strip().split("=", 1)[1]
                                break
        
        # Open in browser
        import webbrowser
        import platform
        
        system = platform.system()
        if system == "Darwin":
            # macOS
            subprocess.run(["open", url])
        elif system == "Linux":
            # Linux - try xdg-open first, then fallback to webbrowser
            try:
                subprocess.run(["xdg-open", url], check=True)
            except:
                webbrowser.open(url)
        else:
            # Windows or other
            webbrowser.open(url)
        
        return {
            "success": True,
            "message": f"Opened frontend in browser",
            "url": url,
            "password": password,
            "hint": "Use the password to access the voice assistant interface"
        }
        
    except Exception as e:
        logger.error(f"Error opening frontend: {e}")
        return {"success": False, "error": str(e)}