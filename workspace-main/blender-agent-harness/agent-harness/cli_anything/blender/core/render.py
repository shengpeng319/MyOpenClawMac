"""Render pipeline - image and animation rendering."""

import os
import tempfile
import subprocess
from typing import Dict, Any

from cli_anything.blender.utils.blender_backend import find_blender


def render_image(
    blend_path: str,
    output_path: str,
    frame: int = 1,
    resolution_x: int = 1920,
    resolution_y: int = 1080,
    engine: str = "BLENDER_EEVEE",
) -> Dict[str, Any]:
    """Render a single image from Blender project.

    Args:
        blend_path: Path to .blend file
        output_path: Output image path (PNG)
        frame: Frame number to render
        resolution_x: Horizontal resolution
        resolution_y: Vertical resolution
        engine: Render engine (BLENDER_EEVEE, CYCLES, BLENDER_WORKBENCH)

    Returns:
        Dict with render status and output path
    """
    if not os.path.exists(blend_path):
        return {"error": f"Blend file not found: {blend_path}"}

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

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
        blender = find_blender()
        result = subprocess.run(
            [blender, "--background", blend_path, "--python", script_path],
            capture_output=True, text=True, timeout=300
        )

        # Check if render succeeded
        if result.returncode != 0:
            return {"error": result.stderr}

        # Verify output file
        if os.path.exists(output_path):
            return {
                "status": "rendered",
                "output_path": output_path,
                "file_size": os.path.getsize(output_path),
                "resolution": f"{resolution_x}x{resolution_y}",
                "engine": engine,
                "frame": frame,
            }
        else:
            return {"error": "Output file not created", "stdout": result.stdout}
    finally:
        os.unlink(script_path)


def render_animation(
    blend_path: str,
    output_dir: str,
    start_frame: int = 1,
    end_frame: int = 250,
    resolution_x: int = 1920,
    resolution_y: int = 1080,
    engine: str = "BLENDER_EEVEE",
) -> Dict[str, Any]:
    """Render an animation from Blender project."""
    if not os.path.exists(blend_path):
        return {"error": f"Blend file not found: {blend_path}"}

    os.makedirs(output_dir, exist_ok=True)

    script = f"""
import bpy

scene = bpy.context.scene
scene.render.filepath = '{output_dir}/frame_####.png'
scene.render.resolution_x = {resolution_x}
scene.render.resolution_y = {resolution_y}
scene.render.image_settings.file_format = 'PNG'
scene.render.engine = '{engine}'

scene.frame_start = {start_frame}
scene.frame_end = {end_frame}

bpy.ops.render.render(animation=True)
print('ANIMATION_OK')
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(script)
        script_path = f.name

    try:
        blender = find_blender()
        result = subprocess.run(
            [blender, "--background", blend_path, "--python", script_path],
            capture_output=True, text=True, timeout=3600
        )

        if result.returncode != 0:
            return {"error": result.stderr}

        # Count frames
        frames = [f for f in os.listdir(output_dir) if f.startswith("frame_") and f.endswith(".png")]
        return {
            "status": "rendered",
            "output_dir": output_dir,
            "frame_count": len(frames),
            "range": f"{start_frame}-{end_frame}",
        }
    finally:
        os.unlink(script_path)
