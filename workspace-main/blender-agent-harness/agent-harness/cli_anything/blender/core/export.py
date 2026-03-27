"""Export pipeline - glTF, FBX, OBJ, USD."""

import os
import tempfile
import subprocess
from typing import Dict, Any

from cli_anything.blender.utils.blender_backend import find_blender


def _run_export_script(blend_path: str, script: str, timeout: int = 300) -> Dict[str, Any]:
    """Helper to run an export script in Blender."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(script)
        script_path = f.name

    try:
        blender = find_blender()
        result = subprocess.run(
            [blender, "--background", blend_path, "--python", script_path],
            capture_output=True, text=True, timeout=timeout
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    finally:
        os.unlink(script_path)


def export_gltf(
    blend_path: str,
    output_path: str,
    export_format: str = "GLB",
) -> Dict[str, Any]:
    """Export scene to glTF 2.0."""
    if not os.path.exists(blend_path):
        return {"error": f"Blend file not found: {blend_path}"}

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    script = f"""
import bpy
import os

output = '{output_path}'
os.makedirs(os.path.dirname(output), exist_ok=True)

bpy.ops.export_scene.gltf(
    filepath=output,
    export_format='{export_format.upper()}',
    use_selection=False,
)
print('GLTF_OK')
"""

    result = _run_export_script(blend_path, script)

    if result["returncode"] != 0:
        return {"error": result["stderr"]}

    if os.path.exists(output_path):
        return {
            "status": "exported",
            "format": "glTF 2.0",
            "output_path": output_path,
            "file_size": os.path.getsize(output_path),
        }
    else:
        return {"error": "Export failed - file not created", "stdout": result["stdout"]}


def export_fbx(blend_path: str, output_path: str) -> Dict[str, Any]:
    """Export scene to FBX."""
    if not os.path.exists(blend_path):
        return {"error": f"Blend file not found: {blend_path}"}

    script = f"""
import bpy
import os

output = '{output_path}'
os.makedirs(os.path.dirname(output), exist_ok=True)

bpy.ops.export_scene.fbx(
    filepath=output,
    use_selection=False,
    bake_space_transform=True,
)
print('FBX_OK')
"""

    result = _run_export_script(blend_path, script)

    if result["returncode"] != 0:
        return {"error": result["stderr"]}

    if os.path.exists(output_path):
        return {
            "status": "exported",
            "format": "FBX",
            "output_path": output_path,
            "file_size": os.path.getsize(output_path),
        }
    else:
        return {"error": "Export failed - file not created", "stdout": result["stdout"]}


def export_obj(blend_path: str, output_path: str) -> Dict[str, Any]:
    """Export scene to OBJ."""
    if not os.path.exists(blend_path):
        return {"error": f"Blend file not found: {blend_path}"}

    script = f"""
import bpy
import os

output = '{output_path}'
os.makedirs(os.path.dirname(output), exist_ok=True)

bpy.ops.scene.obj(
    filepath=output,
    use_selection=False,
    use_normals=True,
    use_materials=True,
)
print('OBJ_OK')
"""

    result = _run_export_script(blend_path, script)

    if result["returncode"] != 0:
        return {"error": result["stderr"]}

    if os.path.exists(output_path):
        return {
            "status": "exported",
            "format": "OBJ",
            "output_path": output_path,
            "file_size": os.path.getsize(output_path),
        }
    else:
        return {"error": "Export failed - file not created", "stdout": result["stdout"]}


def export_usd(blend_path: str, output_path: str) -> Dict[str, Any]:
    """Export scene to USD (Universal Scene Description)."""
    if not os.path.exists(blend_path):
        return {"error": f"Blend file not found: {blend_path}"}

    script = f"""
import bpy
import os

output = '{output_path}'
os.makedirs(os.path.dirname(output), exist_ok=True)

try:
    bpy.ops.wm.usd_export(
        filepath=output,
        export_materials=True,
    )
    print('USD_OK')
except Exception as e:
    print(f'USD export failed: {{e}}')
"""

    result = _run_export_script(blend_path, script)

    if result["returncode"] != 0:
        return {"error": result["stderr"]}

    if os.path.exists(output_path):
        return {
            "status": "exported",
            "format": "USD",
            "output_path": output_path,
            "file_size": os.path.getsize(output_path),
        }
    else:
        return {"error": "Export failed - file not created", "stdout": result["stdout"]}
