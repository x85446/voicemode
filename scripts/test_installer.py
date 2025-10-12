#!/usr/bin/env python3
"""
Test voice-mode-install package across different platforms.

Supports both local Tart VMs and CI environments (Docker/GitHub runners).
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional


class VMTester:
    """Base class for VM testing."""

    def __init__(self, platform: str, wheel_path: Optional[Path] = None,
                 use_pypi: bool = False, pypi_version: Optional[str] = None):
        self.platform = platform
        self.wheel_path = wheel_path
        self.use_pypi = use_pypi
        self.pypi_version = pypi_version
        self.results = {}

    def run_command(self, command: str, timeout: int = 300) -> tuple[int, str, str]:
        """Run a command and return (returncode, stdout, stderr)."""
        raise NotImplementedError

    def test_installer(self) -> dict:
        """Run installer tests and return results."""
        tests = [
            ("cli_help", self._test_cli_help),
            ("dry_run", self._test_dry_run),
            ("platform_detection", self._test_platform_detection),
            ("actual_install", self._test_actual_install),
            ("voicemode_help", self._test_voicemode_help),
            ("voicemode_version", self._test_voicemode_version),
            ("mcp_server_startup", self._test_mcp_server_startup),
        ]

        results = {}
        for test_name, test_func in tests:
            print(f"  Running {test_name}...", end=" ", flush=True)
            try:
                test_func()
                results[test_name] = "PASS"
                print("✓")
            except Exception as e:
                results[test_name] = f"FAIL: {e}"
                print(f"✗ {e}")

        return results

    def _test_import(self):
        """Test that the package can be imported."""
        code, stdout, stderr = self.run_command(
            "export PATH=\"$HOME/.local/bin:$PATH\"; "
            "python3 -c 'import voicemode_install; print(voicemode_install.__version__)'"
        )
        if code != 0:
            raise Exception(f"Import failed: {stderr}")

    def _test_cli_help(self):
        """Test CLI help command."""
        code, stdout, stderr = self.run_command(
            "export PATH=\"$HOME/.local/bin:$PATH\"; "
            "voice-mode-install --help"
        )
        if code != 0 or "VoiceMode Installer" not in stdout:
            raise Exception(f"CLI help failed: {stderr}")

    def _test_dry_run(self):
        """Test dry-run mode."""
        code, stdout, stderr = self.run_command(
            "export PATH=\"$HOME/.local/bin:$PATH\"; "
            "voice-mode-install --dry-run --non-interactive"
        )
        if code != 0 or "DRY RUN" not in stdout:
            raise Exception(f"Dry run failed: {stderr}")

    def _test_platform_detection(self):
        """Test platform detection."""
        code, stdout, stderr = self.run_command(
            "export PATH=\"$HOME/.local/bin:$PATH\"; "
            "voice-mode-install --dry-run --non-interactive"
        )
        if code != 0:
            raise Exception(f"Platform detection failed: {stderr}")

        # Check for platform-specific strings
        platform_strings = {
            "ubuntu": ["Ubuntu", "Debian"],
            "fedora": ["Fedora"],
            "debian": ["Debian", "Ubuntu"],
        }

        expected = platform_strings.get(self.platform, [])
        if expected and not any(s in stdout for s in expected):
            raise Exception(f"Platform not detected correctly. Expected one of {expected}")

    def _test_actual_install(self):
        """Test that voice-mode-install actually installs VoiceMode."""
        # Run the actual installer
        code, stdout, stderr = self.run_command(
            "export PATH=\"$HOME/.local/bin:$PATH\"; "
            "voice-mode-install --non-interactive"
        )
        if code != 0:
            raise Exception(f"Installation failed: {stderr}")

        # Check that installation completed message appears
        if "Installation Complete!" not in stdout and "successfully installed" not in stdout:
            raise Exception("Installation did not report success")

    def _test_voicemode_help(self):
        """Test that voicemode --help works after installation."""
        code, stdout, stderr = self.run_command(
            "export PATH=\"$HOME/.local/bin:$PATH\"; "
            "voicemode --help"
        )
        if code != 0:
            raise Exception(f"voicemode --help failed: {stderr}")

        # Check that help output contains expected content
        if "VoiceMode" not in stdout and "voice" not in stdout.lower():
            raise Exception("voicemode --help output doesn't look right")

    def _test_voicemode_version(self):
        """Test that voicemode --version works after installation."""
        code, stdout, stderr = self.run_command(
            "export PATH=\"$HOME/.local/bin:$PATH\"; "
            "voicemode --version"
        )
        if code != 0:
            raise Exception(f"voicemode --version failed: {stderr}")

        # Check that version output looks reasonable (contains a number)
        if not any(char.isdigit() for char in stdout):
            raise Exception(f"voicemode --version output doesn't contain version number: {stdout}")

    def _test_mcp_server_startup(self):
        """Test that MCP server can start (will timeout quickly but shouldn't crash)."""
        # Try to start the MCP server - it will fail due to no stdin, but shouldn't crash
        code, stdout, stderr = self.run_command(
            "export PATH=\"$HOME/.local/bin:$PATH\"; "
            "timeout 2 voicemode server stdio || true"
        )

        # Check that it didn't crash with an import error or similar
        if "ImportError" in stderr or "ModuleNotFoundError" in stderr:
            raise Exception(f"MCP server has import errors: {stderr}")

        # Check that FFmpeg warning appears (expected)
        if "FFmpeg" not in stderr and "ffmpeg" not in stderr.lower():
            # FFmpeg warning might not always appear, so this is just informational
            pass


class TartVMTester(VMTester):
    """Test using local Tart VMs."""

    def __init__(self, platform: str, wheel_path: Optional[Path] = None, vm_name: Optional[str] = None,
                 clone_fresh: bool = False, use_pypi: bool = False, pypi_version: Optional[str] = None):
        super().__init__(platform, wheel_path, use_pypi, pypi_version)
        self.base_vm_name = vm_name or f"voicemode-test-{platform}"
        self.clone_fresh = clone_fresh
        self.http_server_proc = None
        self.created_vm = False

        if clone_fresh:
            # Create a unique VM name for this test run
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.vm_name = f"{self.base_vm_name}-{timestamp}"
        else:
            self.vm_name = self.base_vm_name

    def setup(self):
        """Set up VM and HTTP server."""
        print(f"Setting up Tart VM: {self.vm_name}")

        # If clone_fresh, create a fresh VM clone
        if self.clone_fresh:
            print(f"  Cloning fresh VM from {self.base_vm_name}...")
            result = subprocess.run(
                ["tart", "clone", self.base_vm_name, self.vm_name],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                raise Exception(f"Failed to clone VM: {result.stderr}")
            self.created_vm = True
            print(f"  Cloned {self.vm_name}")

            # Start the cloned VM
            print(f"  Starting VM {self.vm_name}...")
            subprocess.Popen(
                ["tart", "run", "--no-graphics", self.vm_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # Give it time to boot and start guest agent
            import time
            print(f"  Waiting for VM to boot...")
            time.sleep(15)

        # Start HTTP server for wheel distribution (only if using local wheel)
        if self.wheel_path:
            dist_dir = self.wheel_path.parent
            self.http_server_proc = subprocess.Popen(
                ["python3", "-m", "http.server", "8000"],
                cwd=dist_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"  Started HTTP server on port 8000")

        # Ensure VM is running (skip if we just cloned and started it)
        if not self.clone_fresh:
            result = subprocess.run(
                ["tart", "list"],
                capture_output=True,
                text=True
            )

            if self.vm_name not in result.stdout:
                print(f"  VM {self.vm_name} not found. Available VMs:")
                print(result.stdout)
                raise Exception(f"VM {self.vm_name} not available")

            # Check if VM is running
            if "running" not in result.stdout or self.vm_name not in result.stdout:
                print(f"  Starting VM {self.vm_name}...")
                subprocess.run(["tart", "run", self.vm_name], check=False)

    def teardown(self):
        """Clean up resources."""
        if self.http_server_proc:
            self.http_server_proc.terminate()
            self.http_server_proc.wait()
            print("  Stopped HTTP server")

        # If we created a cloned VM, delete it
        if self.created_vm:
            print(f"  Stopping VM {self.vm_name}...")
            subprocess.run(["tart", "stop", self.vm_name], check=False, capture_output=True)
            print(f"  Deleting VM {self.vm_name}...")
            subprocess.run(["tart", "delete", self.vm_name], check=False, capture_output=True)
            print(f"  Cleaned up VM {self.vm_name}")

    def run_command(self, command: str, timeout: int = 300) -> tuple[int, str, str]:
        """Run command in Tart VM via SSH."""
        # Use tart exec to run commands (no -- separator needed)
        full_command = ["tart", "exec", self.vm_name, "bash", "-c", command]

        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return result.returncode, result.stdout, result.stderr

    def install_prerequisites(self):
        """Install uv and voice-mode-install in VM."""
        print("  Installing prerequisites...")

        # Install uv
        print("    Installing uv...")
        code, stdout, stderr = self.run_command(
            "curl -LsSf https://astral.sh/uv/install.sh | sh"
        )
        if code != 0:
            print(f"    Warning: uv install returned {code}")

        # Add uv to PATH
        code, stdout, stderr = self.run_command(
            "export PATH=\"$HOME/.local/bin:$PATH\"; uv --version"
        )
        if code != 0:
            raise Exception(f"uv not available after install: {stderr}")
        print(f"    uv version: {stdout.strip()}")

        # Install voice-mode-install
        print("    Installing voice-mode-install...")
        if self.use_pypi:
            # Install from PyPI
            package_spec = "voice-mode-install"
            if self.pypi_version:
                package_spec = f"voice-mode-install=={self.pypi_version}"
            print(f"    Installing from PyPI: {package_spec}")

            code, stdout, stderr = self.run_command(
                f"export PATH=\"$HOME/.local/bin:$PATH\"; "
                f"uv tool install {package_spec}"
            )
            if code != 0:
                raise Exception(f"Failed to install from PyPI: {stderr}")
        else:
            # Download and install wheel from host
            print(f"    Downloading {self.wheel_path.name}...")
            code, stdout, stderr = self.run_command(
                f"curl -o /tmp/{self.wheel_path.name} http://192.168.64.1:8000/{self.wheel_path.name}"
            )
            if code != 0:
                raise Exception(f"Failed to download wheel: {stderr}")

            code, stdout, stderr = self.run_command(
                f"export PATH=\"$HOME/.local/bin:$PATH\"; "
                f"uv tool install /tmp/{self.wheel_path.name}"
            )
            if code != 0:
                raise Exception(f"Failed to install wheel: {stderr}")

        # Verify installation
        print("    Verifying installation...")
        code, stdout, stderr = self.run_command(
            f"export PATH=\"$HOME/.local/bin:$PATH\"; "
            f"voice-mode-install --version"
        )
        if code != 0:
            raise Exception(f"Installation verification failed: {stderr}")
        print(f"    Installed: {stdout.strip()}")


class DockerTester(VMTester):
    """Test using Docker containers (for CI)."""

    def __init__(self, platform: str, wheel_path: Optional[Path] = None,
                 use_pypi: bool = False, pypi_version: Optional[str] = None):
        super().__init__(platform, wheel_path, use_pypi, pypi_version)
        self.container_name = f"voicemode-test-{platform}"
        self.image = self._get_image()

    def _get_image(self) -> str:
        """Get Docker image for platform."""
        images = {
            "ubuntu": "ubuntu:22.04",
            "debian": "debian:12",
            "fedora": "fedora:39",
        }
        return images.get(self.platform, "ubuntu:22.04")

    def setup(self):
        """Set up Docker container."""
        print(f"Setting up Docker container: {self.image}")

        # Start container
        docker_args = [
            "docker", "run", "-d",
            "--name", self.container_name
        ]

        # Only mount volume if using local wheel
        if self.wheel_path:
            docker_args.extend(["-v", f"{self.wheel_path.parent}:/dist:ro"])

        docker_args.extend([self.image, "sleep", "infinity"])

        subprocess.run(docker_args, check=True)
        print(f"  Started container {self.container_name}")

    def teardown(self):
        """Clean up Docker container."""
        subprocess.run(
            ["docker", "rm", "-f", self.container_name],
            check=False,
            capture_output=True
        )
        print(f"  Removed container {self.container_name}")

    def run_command(self, command: str, timeout: int = 300) -> tuple[int, str, str]:
        """Run command in Docker container."""
        result = subprocess.run(
            ["docker", "exec", self.container_name, "bash", "-c", command],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr

    def install_prerequisites(self):
        """Install uv and voice-mode-install in container."""
        print("  Installing prerequisites...")

        # Install curl and python3
        if self.platform == "ubuntu" or self.platform == "debian":
            self.run_command("apt-get update && apt-get install -y curl python3")
        elif self.platform == "fedora":
            self.run_command("dnf install -y curl python3")

        # Install uv
        code, stdout, stderr = self.run_command(
            "curl -LsSf https://astral.sh/uv/install.sh | sh"
        )
        if code != 0:
            raise Exception(f"Failed to install uv: {stderr}")

        # Install voice-mode-install
        if self.use_pypi:
            # Install from PyPI
            package_spec = "voice-mode-install"
            if self.pypi_version:
                package_spec = f"voice-mode-install=={self.pypi_version}"
            print(f"    Installing from PyPI: {package_spec}")

            code, stdout, stderr = self.run_command(
                f"export PATH=\"$HOME/.local/bin:$PATH\"; "
                f"uv tool install {package_spec}"
            )
            if code != 0:
                raise Exception(f"Failed to install from PyPI: {stderr}")
        else:
            # Install local wheel
            code, stdout, stderr = self.run_command(
                f"export PATH=\"$HOME/.local/bin:$PATH\"; "
                f"uv tool install /dist/{self.wheel_path.name}"
            )
            if code != 0:
                raise Exception(f"Failed to install wheel: {stderr}")

        # Verify installation
        code, stdout, stderr = self.run_command(
            f"export PATH=\"$HOME/.local/bin:$PATH\"; "
            f"voice-mode-install --version"
        )
        if code != 0:
            raise Exception(f"Installation verification failed: {stderr}")


def main():
    parser = argparse.ArgumentParser(description="Test voice-mode-install package")
    parser.add_argument(
        "platform",
        choices=["ubuntu", "debian", "fedora"],
        help="Platform to test on"
    )
    parser.add_argument(
        "--wheel",
        type=Path,
        help="Path to wheel file (mutually exclusive with --pypi)"
    )
    parser.add_argument(
        "--pypi",
        action="store_true",
        help="Install from PyPI instead of local wheel"
    )
    parser.add_argument(
        "--pypi-version",
        help="Specific version to install from PyPI (e.g., 5.1.6)"
    )
    parser.add_argument(
        "--backend",
        choices=["tart", "docker"],
        default="tart",
        help="Testing backend (default: tart)"
    )
    parser.add_argument(
        "--vm-name",
        help="Tart VM name (default: voicemode-test-{platform})"
    )
    parser.add_argument(
        "--clone-fresh",
        action="store_true",
        help="Clone a fresh VM for testing (Tart only)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output results to JSON file"
    )

    args = parser.parse_args()

    # Validate arguments
    if args.wheel and args.pypi:
        print("Error: --wheel and --pypi are mutually exclusive")
        return 1

    if not args.wheel and not args.pypi:
        print("Error: Either --wheel or --pypi must be specified")
        return 1

    if args.wheel and not args.wheel.exists():
        print(f"Error: Wheel file not found: {args.wheel}")
        return 1

    # Create tester
    if args.backend == "tart":
        tester = TartVMTester(args.platform, args.wheel, args.vm_name, args.clone_fresh, args.pypi, args.pypi_version)
    else:
        tester = DockerTester(args.platform, args.wheel, args.pypi, args.pypi_version)

    try:
        # Setup
        print(f"\n=== Testing {args.platform} with {args.backend} backend ===\n")
        tester.setup()
        tester.install_prerequisites()

        # Run tests
        print("\nRunning tests:")
        results = tester.test_installer()

        # Summary
        print("\n=== Results ===")
        passed = sum(1 for v in results.values() if v == "PASS")
        total = len(results)
        print(f"Passed: {passed}/{total}")

        for test, result in results.items():
            status = "✓" if result == "PASS" else "✗"
            print(f"  {status} {test}: {result}")

        # Save results
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to {args.output}")

        # Return exit code
        return 0 if passed == total else 1

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        tester.teardown()


if __name__ == "__main__":
    sys.exit(main())
