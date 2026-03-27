"""Project management - create, open, save, info."""

import json
import os
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

from cli_anything.blender.utils.blender_backend import find_blender


def create_project(name: str, output_dir: str, **options) -> Dict[str, Any]:
    """Create a new Blender project with default cube."""
    output_path = Path(output_dir) / f"{name}.blend"
    os.makedirs(output_dir, exist_ok=True)

    script = f"""
import bpy

# Create new scene with default cube
bpy.ops.mesh.primitive_cube_add()

# Save as .blend file
bpy.ops.wm.save_as_mainfile(filepath='{output_path}')
print('CREATED:{output_path}')
"""

    # Write temp script
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(script)
        script_path = f.name

    try:
        blender = find_blender()
        result = subprocess.run(
            [blender, "--background", "--python", script_path],
            capture_output=True, text=True, timeout=60
        )

        if result.returncode != 0:
            return {"error": result.stderr, "returncode": result.returncode}

        # Write state file
        state = {"name": name, "type": "blender", "version": "0.1.0", "path": str(output_path)}
        json_path = output_path.with_suffix(".blend-cli.json")
        with open(json_path, "w") as f:
            json.dump(state, f, indent=2)

        return {"project_path": str(output_path), "state_path": str(json_path), "name": name}
    finally:
        os.unlink(script_path)


def open_project(project_path: str) -> Dict[str, Any]:
    """Open an existing Blender project."""
    path = Path(project_path)
    if not path.exists():
        return {"error": f"Project not found: {project_path}"}

    state_path = path.with_suffix(".blend-cli.json")
    if state_path.exists():
        with open(state_path) as f:
            state = json.load(f)
        return {"status": "opened", "project": state}

    return {"status": "opened", "project": {"name": path.stem, "path": str(path)}}


def save_project(project_path: str) -> Dict[str, Any]:
    """Save the current Blender project."""
    script = f"""
import bpy
bpy.ops.wm.save_as_mainfile(filepath='{project_path}')
print('SAVED:{project_path}')
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(script)
        script_path = f.name

    try:
        blender = find_blender()
        result = subprocess.run(
            [blender, "--background", "--python", script_path],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            return {"error": result.stderr}
        return {"status": "saved", "path": project_path}
    finally:
        os.unlink(script_path)


def project_info(project_path: str) -> Dict[str, Any]:
    """Get project metadata."""
    path = Path(project_path)
    if not path.exists():
        return {"error": f"Project not found: {project_path}"}

    script = """
import bpy
import json

info = {
    "name": bpy.data.filepath.split("/")[-1] if bpy.data.filepath else "unsaved",
    "scenes": len(bpy.data.scenes),
    "objects": len(bpy.data.objects),
}
print(json.dumps(info))
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(script)
        script_path = f.name

    try:
        blender = find_blender()
        result = subprocess.run(
            [blender, "--background", project_path, "--python", script_path],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            return {"path": str(path), "size_bytes": path.stat().st_size}

        try:
            info = json.loads(result.stdout.strip().split("\\n")[-1])
            info["path"] = str(path)
            info["size_bytes"] = path.stat().st_size
            return info
        except:
            return {"path": str(path), "size_bytes": path.stat().st_size}
    finally:
        os.unlink(script_path)
