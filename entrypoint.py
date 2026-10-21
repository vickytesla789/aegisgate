"""Unified entry point for AegisGate standalone executable and server.

Supports:
- Running as a GUI / server process by default (uvicorn server on 127.0.0.1:8000).
- Running CLI maintenance commands (verify-audit, backup-db, init-admin, diagnostics)
  when arguments are provided.
- Calls multiprocessing.freeze_support() for Windows binary compatibility.
"""

import multiprocessing
import sys

from app.config import settings

CLI_COMMANDS = {
    "init-admin",
    "reset-password",
    "verify-audit",
    "backup-db",
    "verify-backup",
    "restore-db",
    "diagnostics",
}


def main():
    multiprocessing.freeze_support()

    # If first argument is a recognized CLI command, delegate to app.cli
    if len(sys.argv) > 1 and sys.argv[1] in CLI_COMMANDS:
        from app.cli import main as cli_main
        cli_main()
        return

    # If --help is requested without a command
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        print("AegisGate — Offline-First AI Security Gateway")
        print("\nUsage:")
        print("  aegisgate.exe                Start web server on 127.0.0.1:8000")
        print("  aegisgate.exe [command]      Execute administrative CLI command")
        print("\nAvailable CLI commands:")
        for cmd in sorted(CLI_COMMANDS):
            print(f"  {cmd}")
        print("\nFor command-specific help: aegisgate.exe [command] --help")
        return

    # Default action: Launch the AegisGate server
    from app.main import run
    run()


if __name__ == "__main__":
    main()
