"""Unified REPL skin for CLI-Anything interactive mode."""

import sys
from typing import Dict, Any, Optional
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.history import FileHistory

# Styling
STYLE = Style.from_dict({
    "banner": "ansigray",
    "software": "ansiblue bold",
    "version": "ansigreen",
    "prompt": "ansicyan",
    "command": "ansiyellow",
    "success": "ansigreen",
    "error": "ansired",
    "warning": "ansiyellow",
    "info": "ansiblue",
    "key": "ansicyan",
    "value": "ansigray",
    "table-header": "ansicyan bold",
})


class ReplSkin:
    """Unified REPL interface with branded banner, prompts, and output helpers."""

    def __init__(self, software: str, version: str = "1.0.0"):
        self.software = software
        self.version = version
        self.history_file = f".{software}-cli-history"

    def print_banner(self):
        """Display branded startup banner."""
        banner = f"""
╔══════════════════════════════════════════════════════╗
║  {self.software.upper()}-CLI  v{self.version}   (type 'help' for commands)  ║
╚══════════════════════════════════════════════════════╝
"""
        print(banner)

    def create_prompt_session(self, project_name: Optional[str] = None) -> PromptSession:
        """Create prompt_toolkit session with history."""
        history = FileHistory(self.history_file)
        return PromptSession(history=history)

    def get_input(
        self,
        session: PromptSession,
        project_name: Optional[str] = None,
        modified: bool = False,
    ) -> str:
        """Get user input with styled prompt."""
        prompt_str = f"{self.software}> "
        if project_name:
            indicator = " *" if modified else ""
            prompt_str = f"[{project_name}{indicator}] {self.software}> "
        return session.prompt(prompt_str)

    def help(self, commands: Dict[str, str]):
        """Display formatted help."""
        print("\nAvailable commands:")
        print("-" * 50)
        for cmd, desc in commands.items():
            print(f"  {cmd:20s} {desc}")
        print()

    def success(self, message: str):
        """Print success message."""
        print(f"✓ {message}")

    def error(self, message: str):
        """Print error message."""
        print(f"✗ Error: {message}", file=sys.stderr)

    def warning(self, message: str):
        """Print warning message."""
        print(f"⚠ {message}")

    def info(self, message: str):
        """Print info message."""
        print(f"● {message}")

    def status(self, key: str, value: str):
        """Print key-value status line."""
        print(f"  {key}: {value}")

    def table(self, headers: list, rows: list):
        """Print formatted table."""
        col_widths = [max(len(str(row[i])) for row in rows + [headers]) for i in range(len(headers))]
        header_line = "  ".join(h.ljust(w) for h, w in zip(headers, col_widths))
        print(header_line)
        print("-" * len(header_line))
        for row in rows:
            print("  ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths)))

    def progress(self, current: int, total: int, message: str = ""):
        """Print progress bar."""
        bar_len = 30
        filled = int(bar_len * current / total)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"\r[{bar}] {current}/{total} {message}", end="", flush=True)
        if current >= total:
            print()

    def print_goodbye(self):
        """Display styled exit message."""
        print(f"\n[{self.software}] Goodbye!\n")
