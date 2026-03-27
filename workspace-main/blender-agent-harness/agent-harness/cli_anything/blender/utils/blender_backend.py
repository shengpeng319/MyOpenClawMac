"""Blender subprocess backend - invokes real Blender."""

import os
import shutil
import subprocess
import tempfile
import json
from pathlib import Path
from typing import Optional, Dict, Any

BLENDER_NOT_FOUND_MSG = """
Blender is not installed or not in PATH.

Install Blender:
  macOS:   brew install blender
  Ubuntu:  sudo apt install blender
  Windows: Download from https://blender.org

After installation, verify with: blender --version
"""


def find_blender() -> str:
    """Find Blender executable. Raises RuntimeError if not found."""
    path = shutil.which("blender")
    if path:
        return path
    raise RuntimeError(BLENDER_NOT_FOUND_MSG)


def run_blender_script(
    script: str,
    blend_path: Optional[str] = None,
    background: bool = True,
    timeout: int = 300,
) -> Dict[str, Any]:
    """Run a Python script in Blender.

    Args:
        script: Python code to execute in Blender
        blend_path: Optional .blend file to open first
        background: Run in background (headless) mode
        timeout: Timeout in seconds

    Returns:
        Dict with returncode, stdout, stderr
    """
    blender = find_blender()

    # Write script to temp file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(script)
        script_path = f.name

    args = [blender]
    if background:
        args.append("--background")

    if blend_path:
        args.extend(["--python", script_path, "--", blend_path])
    else:
        args.extend(["--python", script_path])

    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    finally:
        os.unlink(script_path)


def run_blender_script_file(
    script_path: str,
    blend_path: Optional[str] = None,
    background: bool = True,
    timeout: int = 300,
) -> Dict[str, Any]:
    """Run a Python script file in Blender.

    Args:
        script_path: Path to .py script file
        blend_path: Optional .blend file to open first
        background: Run in background mode
        timeout: Timeout in seconds

    Returns:
        Dict with returncode, stdout, stderr
    """
    blender = find_blender()
    args = [blender]

    if background:
        args.append("--background")

    if blend_path:
        args.extend(["--python", script_path, "--", blend_path])
    else:
        args.extend(["--python", script_path])

    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def render_image(
    blend_path: str,
    output_path: str,
    frame: int = 1,
    resolution_x: int = 1920,
    resolution_y: int = 1080,
    engine: str = "BLENDER_EEVEE",
) -> Dict[str, Any]:
    """Render an image from a Blender project."""
    blender = find_blender()

    script = f"""
import bpy

scene = bpy.context.scene
scene.render.filepath = '{output_path}'
scene.render.resolution_x = {resolution_x}
scene.render.resolution_y = {resolution_y}
scene.render.image_settings.file_format = 'PNG'
scene.render.engine = '{engine}'

scene.frame_set({frame})
bpy.ops.render.render(write_still=True)
print('RENDER_OK')
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(script)
        script_path = f.name

    try:
        args = [blender, "--background", blend_path, "--python", script_path]
        result = subprocess.run(args, capture_output=True, text=True, timeout=300)
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "output_path": output_path if result.returncode == 0 else None,
        }
    finally:
        os.unlink(script_path)


def export_gltf(blend_path: str, output_path: str) -> Dict[str, Any]:
    """Export Blender scene to glTF 2.0."""
    blender = find_blender()
    script = f"""
import bpy
import os

os.makedirs(os.path.dirname('{output_path}'), exist_ok=True)

bpy.ops.export_scene.gltf(
    filepath='{output_path}',
    export_format='GLB',
    use_selection=False
)
print('GLTF_OK')
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(script)
        script_path = f.name

    try:
        args = [blender, "--background", blend_path, "--python", script_path]
        result = subprocess.run(args, capture_output=True, text=True, timeout=300)
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "output_path": output_path if result.returncode == 0 else None,
        }
    finally:
        os.unlink(script_path)


def export_fbx(blend_path: str, output_path: str) -> Dict[str, Any]:
    """Export Blender scene to FBX."""
    blender = find_blender()
    script = f"""
import bpy
import os

os.makedirs(os.path.dirname('{output_path}'), exist_ok=True)

bpy.ops.export_scene.fbx(
    filepath='{output_path}',
    use_selection=False,
    bake_space_transform=True,
    object_types={{'MESH', 'EMPTY', 'CAMERA', 'LIGHT'}},
)
print('FBX_OK')
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(script)
        script_path = f.name

    try:
        args = [blender, "--background", blend_path, "--python", script_path]
        result = subprocess.run(args, capture_output=True, text=True, timeout=300)
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "output_path": output_path if result.returncode == 0 else None,
        }
    finally:
        os.unlink(script_path)


def export_obj(blend_path: str, output_path: str) -> Dict[str, Any]:
    """Export Blender scene to OBJ (if addon available)."""
    blender = find_blender()
    script = f"""
import bpy
import os

os.makedirs(os.path.dirname('{output_path}'), exist_ok=True)

# Try scene.obj first (Blender 5.x)
try:
    bpy.ops.scene.obj(filepath='{output_path}', use_selection=False)
    print('OBJ_OK')
except:
    # Fallback to export_scene.obj
    try:
        bpy.ops.export_scene.obj(filepath='{output_path}', use_selection=False)
        print('OBJ_OK')
    except Exception as e:
        print(f'OBJ export not available: {{e}}')
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(script)
        script_path = f.name

    try:
        args = [blender, "--background", blend_path, "--python", script_path]
        result = subprocess.run(args, capture_output=True, text=True, timeout=300)
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "output_path": output_path if result.returncode == 0 else None,
        }
    finally:
        os.unlink(script_path)
