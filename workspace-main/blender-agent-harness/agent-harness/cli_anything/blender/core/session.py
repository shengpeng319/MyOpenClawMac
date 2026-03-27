"""Session state management - undo, redo, status."""

import json
from typing import Dict, Any, Optional
from pathlib import Path


class Session:
    """In-memory session state for Blender CLI."""

    def __init__(self):
        self.current_project: Optional[str] = None
        self.current_scene: str = "Scene"
        self.current_object: Optional[str] = None
        self.history: list = []
        self.history_index: int = -1
        self.modified: bool = False

    def set_project(self, project_path: str):
        """Set current project."""
        self.current_project = project_path
        self.modified = False
        self.history = []
        self.history_index = -1

    def push_state(self, action: str, data: Dict[str, Any]):
        """Push state to history for undo/redo."""
        # Truncate redo history
        self.history = self.history[: self.history_index + 1]
        self.history.append({"action": action, "data": data})
        self.history_index = len(self.history) - 1
        self.modified = True

    def undo(self) -> Optional[Dict[str, Any]]:
        """Undo last action."""
        if self.history_index >= 0:
            state = self.history[self.history_index]
            self.history_index -= 1
            return state
        return None

    def redo(self) -> Optional[Dict[str, Any]]:
        """Redo previously undone action."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            return self.history[self.history_index]
        return None

    def status(self) -> Dict[str, Any]:
        """Get current session status."""
        return {
            "project": self.current_project,
            "scene": self.current_scene,
            "current_object": self.current_object,
            "modified": self.modified,
            "history_count": len(self.history),
            "history_index": self.history_index,
        }

    def save_state(self, path: str):
        """Save session state to file."""
        state = {
            "current_project": self.current_project,
            "current_scene": self.current_scene,
            "current_object": self.current_object,
            "modified": self.modified,
        }
        with open(path, "w") as f:
            json.dump(state, f, indent=2)

    def load_state(self, path: str) -> bool:
        """Load session state from file."""
        try:
            with open(path) as f:
                state = json.load(f)
            self.current_project = state.get("current_project")
            self.current_scene = state.get("current_scene", "Scene")
            self.current_object = state.get("current_object")
            self.modified = state.get("modified", False)
            return True
        except:
            return False


# Global session instance
_session = Session()


def get_session() -> Session:
    """Get the global session instance."""
    return _session
