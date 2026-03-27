"""Object manipulation - add, delete, list, transform."""

import json
from typing import Dict, Any, List, Optional

from cli_anything.blender.utils.blender_backend import run_blender_script, find_blender


def add_object(
    object_type: str,
    location: tuple = (0, 0, 0),
    rotation: tuple = (0, 0, 0),
    scale: tuple = (1, 1, 1),
    name: Optional[str] = None,
) -> Dict[str, Any]:
    """Add an object to the scene."""
    object_type = object_type.lower().replace("-", "_").replace(" ", "_")

    type_map = {
        "cube": "primitive_cube_add",
        "sphere": "primitive_uv_sphere_add",
        "plane": "primitive_plane_add",
        "cylinder": "primitive_cylinder_add",
        "cone": "primitive_cone_add",
        "torus": "primitive_torus_add",
        "uv_sphere": "primitive_uv_sphere_add",
        "ico_sphere": "primitive_ico_sphere_add",
        "grid": "primitive_grid_add",
        "monkey": "primitive_monkey_add",
        "text": "primitive_text_add",
    }

    op_func = type_map.get(object_type, f"primitive_{object_type}_add")
    obj_name = name or f"{object_type.capitalize()}"
    loc_str = f"({location[0]}, {location[1]}, {location[2]})"
    rot_str = f"({rotation[0]}, {rotation[1]}, {rotation[2]})"
    scale_str = f"({scale[0]}, {scale[1]}, {scale[2]})"

    script = f"""
import bpy

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.{op_func}(location={loc_str}, rotation={rot_str}, scale={scale_str})

if bpy.context.active_object:
    bpy.context.active_object.name = '{obj_name}'

print('Object added: {obj_name}')
"""

    result = run_blender_script(script, background=True)

    if result["returncode"] != 0:
        return {"error": result["stderr"], "returncode": result["returncode"]}

    return {
        "status": "added",
        "name": obj_name,
        "type": object_type,
        "location": location,
        "rotation": rotation,
        "scale": scale,
    }


def delete_object(object_name: str) -> Dict[str, Any]:
    """Delete an object by name."""
    script = f"""
import bpy

obj = bpy.data.objects.get('{object_name}')
if obj is None:
    print('Error: Object not found: {object_name}')
else:
    bpy.data.objects.remove(obj, do_unlink=True)
    print('Deleted: {object_name}')
"""

    result = run_blender_script(script, background=True)

    if result["returncode"] != 0:
        return {"error": result["stderr"]}

    if "Error" in result["stdout"]:
        return {"error": result["stdout"]}

    return {"status": "deleted", "name": object_name}


def list_objects() -> Dict[str, Any]:
    """List all objects in the current scene."""
    script = """
import bpy
import json
import math

objects = []
for obj in bpy.data.objects:
    objects.append({
        "name": obj.name,
        "type": obj.type,
        "location": [round(x, 4) for x in obj.location],
        "rotation": [round(math.degrees(a), 2) for a in obj.rotation_euler],
        "scale": [round(x, 4) for x in obj.scale],
    })

print(json.dumps(objects))
"""

    result = run_blender_script(script, background=True)

    if result["returncode"] != 0:
        return {"error": result["stderr"]}

    try:
        objects = json.loads(result["stdout"].strip().split(chr(10))[0])
        return {"objects": objects, "count": len(objects)}
    except Exception as e:
        return {"objects": [], "error": f"Failed to parse object list"}


def transform_object(
    object_name: str,
    location: Optional[tuple] = None,
    rotation: Optional[tuple] = None,
    scale: Optional[tuple] = None,
) -> Dict[str, Any]:
    """Transform an object (move, rotate, scale)."""
    updates = []
    if location is not None:
        updates.append(f"obj.location = ({location[0]}, {location[1]}, {location[2]})")
    if rotation is not None:
        updates.append(f"obj.rotation_euler = (math.radians({rotation[0]}), math.radians({rotation[1]}), math.radians({rotation[2]}))")
    if scale is not None:
        updates.append(f"obj.scale = ({scale[0]}, {scale[1]}, {scale[2]})")

    script = f"""
import bpy
import math

obj = bpy.data.objects.get('{object_name}')
if obj is None:
    print('Error: Object not found: {object_name}')
else:
    {chr(10).join(updates)}
    print('Transformed: {object_name}')
"""

    result = run_blender_script(script, background=True)

    if result["returncode"] != 0:
        return {"error": result["stderr"]}

    if "Error" in result["stdout"]:
        return {"error": result["stdout"]}

    return {
        "status": "transformed",
        "name": object_name,
        "location": location,
        "rotation": rotation,
        "scale": scale,
    }
