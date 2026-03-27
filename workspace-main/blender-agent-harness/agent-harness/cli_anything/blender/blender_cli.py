"""Blender CLI - main entry point with Click + REPL."""

import os
import sys
import json
import click
from typing import Optional

from cli_anything.blender.utils.blender_backend import (
    find_blender,
    render_image as backend_render_image,
    export_gltf as backend_export_gltf,
    export_fbx as backend_export_fbx,
    export_obj as backend_export_obj,
)
from cli_anything.blender.core.project import (
    create_project,
    open_project,
    save_project,
    project_info,
)
from cli_anything.blender.core.object import (
    add_object,
    delete_object,
    list_objects,
    transform_object,
)
from cli_anything.blender.core.render import (
    render_image,
    render_animation,
)
from cli_anything.blender.core.export import (
    export_gltf,
    export_fbx,
    export_obj,
    export_usd,
)
from cli_anything.blender.core.session import get_session
from cli_anything.blender.utils.repl_skin import ReplSkin


# Global session and skin
session = get_session()
skin = ReplSkin("blender", version="0.1.0")


def json_output(result: dict) -> str:
    """Format result as JSON."""
    return json.dumps(result, indent=2, default=str)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Blender CLI - AI-friendly interface for Blender 3D.

    Run without subcommands to enter interactive REPL mode.
    """
    if ctx.invoked_subcommand is None:
        # Enter REPL mode
        ctx.invoke(repl)
    else:
        # Check if Blender is installed for commands that need it
        try:
            find_blender()
        except RuntimeError as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)


@cli.command()
def repl():
    """Enter interactive REPL mode."""
    skin.print_banner()

    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import FileHistory

    session_history = FileHistory(".blender-cli-history")
    prompt_session = PromptSession(history=session_history)

    commands = {
        "help": "Show this help message",
        "project new <name>": "Create new project",
        "project open <path>": "Open existing project",
        "project save": "Save current project",
        "project info": "Show project info",
        "object add <type>": "Add object (cube/sphere/plane/...)",
        "object list": "List all objects",
        "object delete <name>": "Delete object",
        "render image <path>": "Render to image",
        "export gltf <path>": "Export to glTF",
        "export fbx <path>": "Export to FBX",
        "exit/quit": "Exit REPL",
    }

    while True:
        try:
            line = prompt_session.prompt("blender> ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not line:
            continue

        parts = line.split()
        cmd = parts[0].lower()

        if cmd in ("exit", "quit", "q"):
            break
        elif cmd == "help":
            skin.help(commands)
        elif cmd == "project":
            if len(parts) < 2:
                click.echo("Usage: project new <name> | open <path> | save | info")
            elif parts[1] == "new" and len(parts) >= 3:
                result = create_project(parts[2], os.getcwd())
                click.echo(json_output(result))
            elif parts[1] == "open" and len(parts) >= 3:
                result = open_project(parts[2])
                if "error" not in result:
                    session.set_project(parts[2])
                click.echo(json_output(result))
            elif parts[1] == "save":
                if not session.current_project:
                    click.echo("No project open")
                else:
                    result = save_project(session.current_project)
                    click.echo(json_output(result))
            elif parts[1] == "info":
                if not session.current_project:
                    click.echo("No project open")
                else:
                    result = project_info(session.current_project)
                    click.echo(json_output(result))
        elif cmd == "object":
            if len(parts) < 2:
                click.echo("Usage: object add <type> | list | delete <name>")
            elif parts[1] == "add" and len(parts) >= 3:
                result = add_object(parts[2])
                click.echo(json_output(result))
            elif parts[1] == "list":
                result = list_objects()
                click.echo(json_output(result))
            elif parts[1] == "delete" and len(parts) >= 3:
                result = delete_object(parts[2])
                click.echo(json_output(result))
        elif cmd == "render":
            if len(parts) < 3:
                click.echo("Usage: render image <output_path>")
            elif parts[1] == "image":
                if not session.current_project:
                    click.echo("No project open")
                else:
                    result = render_image(session.current_project, parts[2])
                    click.echo(json_output(result))
        elif cmd == "export":
            if len(parts) < 3:
                click.echo("Usage: export gltf/fbx/obj <path>")
            elif parts[1] == "gltf":
                if not session.current_project:
                    click.echo("No project open")
                else:
                    result = export_gltf(session.current_project, parts[2])
                    click.echo(json_output(result))
            elif parts[1] == "fbx":
                if not session.current_project:
                    click.echo("No project open")
                else:
                    result = export_fbx(session.current_project, parts[2])
                    click.echo(json_output(result))
            elif parts[1] == "obj":
                if not session.current_project:
                    click.echo("No project open")
                else:
                    result = export_obj(session.current_project, parts[2])
                    click.echo(json_output(result))
        else:
            click.echo(f"Unknown command: {cmd}. Type 'help' for commands.")

    skin.print_goodbye()


# ============== PROJECT COMMANDS ==============

@cli.group("project")
def project():
    """Project management commands."""
    pass


@project.command("new")
@click.argument("name")
@click.option("--output", "-o", default=".", help="Output directory")
def project_new(name: str, output: str):
    """Create a new Blender project."""
    result = create_project(name, output)
    if "--json" in sys.argv:
        click.echo(json_output(result))
    else:
        if "error" in result:
            click.echo(f"Error: {result['error']}", err=True)
        else:
            click.echo(f"Created: {result['project_path']}")


@project.command("open")
@click.argument("path")
def project_open(path: str):
    """Open an existing Blender project."""
    result = open_project(path)
    if "error" not in result:
        session.set_project(path)
    click.echo(json_output(result) if "--json" in sys.argv else f"Opened: {path}")


@project.command("save")
def project_save():
    """Save the current project."""
    if not session.current_project:
        click.echo("No project open", err=True)
        sys.exit(1)
    result = save_project(session.current_project)
    click.echo(json_output(result))


@project.command("info")
def project_info_cmd():
    """Show project information."""
    if not session.current_project:
        click.echo("No project open", err=True)
        sys.exit(1)
    result = project_info(session.current_project)
    click.echo(json_output(result))


# ============== OBJECT COMMANDS ==============

@cli.group("object")
def object_cmd():
    """Object manipulation commands."""
    pass


@object_cmd.command("add")
@click.argument("type")
@click.option("--name", "-n", help="Object name")
@click.option("--location", "-l", default="0,0,0", help="Location (x,y,z)")
@click.option("--scale", "-s", default="1,1,1", help="Scale (x,y,z)")
def object_add(type: str, name: Optional[str], location: str, scale: str):
    """Add an object to the scene."""
    loc = tuple(float(x) for x in location.split(","))
    scl = tuple(float(x) for x in scale.split(","))
    result = add_object(type, location=loc, scale=scl, name=name)
    click.echo(json_output(result))


@object_cmd.command("list")
def object_list():
    """List all objects in the scene."""
    result = list_objects()
    click.echo(json_output(result))


@object_cmd.command("delete")
@click.argument("name")
def object_delete(name: str):
    """Delete an object."""
    result = delete_object(name)
    click.echo(json_output(result))


@object_cmd.command("transform")
@click.argument("name")
@click.option("--location", "-l", help="Location (x,y,z)")
@click.option("--rotation", "-r", help="Rotation (x,y,z) in degrees")
@click.option("--scale", "-s", help="Scale (x,y,z)")
def object_transform(name: str, location: Optional[str], rotation: Optional[str], scale: Optional[str]):
    """Transform an object."""
    loc = tuple(float(x) for x in location.split(",")) if location else None
    rot = tuple(float(x) for x in rotation.split(",")) if rotation else None
    scl = tuple(float(x) for x in scale.split(",")) if scale else None
    result = transform_object(name, location=loc, rotation=rot, scale=scl)
    click.echo(json_output(result))


# ============== RENDER COMMANDS ==============

@cli.group("render")
def render():
    """Render commands."""
    pass


@render.command("image")
@click.argument("output_path")
@click.option("--project", "-p", help="Blend file path")
@click.option("--frame", "-f", default=1, help="Frame number")
@click.option("--resolution", "-r", default="1920x1080", help="Resolution (WIDTHxHEIGHT)")
def render_image_cmd(output_path: str, project: Optional[str], frame: int, resolution: str):
    """Render an image."""
    blend = project or session.current_project
    if not blend:
        click.echo("No project specified and none open", err=True)
        sys.exit(1)

    res_parts = resolution.split("x")
    res_x = int(res_parts[0])
    res_y = int(res_parts[1]) if len(res_parts) > 1 else 1080

    result = render_image(blend, output_path, frame=frame, resolution_x=res_x, resolution_y=res_y)
    click.echo(json_output(result))


# ============== EXPORT COMMANDS ==============

@cli.group("export")
def export():
    """Export commands."""
    pass


@export.command("gltf")
@click.argument("output_path")
@click.option("--project", "-p", help="Blend file path")
def export_gltf_cmd(output_path: str, project: Optional[str]):
    """Export to glTF 2.0."""
    blend = project or session.current_project
    if not blend:
        click.echo("No project specified and none open", err=True)
        sys.exit(1)
    result = export_gltf(blend, output_path)
    click.echo(json_output(result))


@export.command("fbx")
@click.argument("output_path")
@click.option("--project", "-p", help="Blend file path")
def export_fbx_cmd(output_path: str, project: Optional[str]):
    """Export to FBX."""
    blend = project or session.current_project
    if not blend:
        click.echo("No project specified and none open", err=True)
        sys.exit(1)
    result = export_fbx(blend, output_path)
    click.echo(json_output(result))


@export.command("obj")
@click.argument("output_path")
@click.option("--project", "-p", help="Blend file path")
def export_obj_cmd(output_path: str, project: Optional[str]):
    """Export to OBJ."""
    blend = project or session.current_project
    if not blend:
        click.echo("No project specified and none open", err=True)
        sys.exit(1)
    result = export_obj(blend, output_path)
    click.echo(json_output(result))


# ============== SESSION COMMANDS ==============

@cli.group("session")
def session_cmd():
    """Session management commands."""
    pass


@session_cmd.command("status")
def session_status():
    """Show current session status."""
    result = session.status()
    click.echo(json_output(result))


@session_cmd.command("undo")
def session_undo():
    """Undo last action."""
    result = session.undo()
    click.echo(json_output(result) if result else "Nothing to undo")


@session_cmd.command("redo")
def session_redo():
    """Redo previously undone action."""
    result = session.redo()
    click.echo(json_output(result) if result else "Nothing to redo")


if __name__ == "__main__":
    cli()
