# Blender CLI-Anything

AI-Agent-friendly CLI interface for Blender 3D.

## Installation

```bash
cd blender-agent-harness/agent-harness
pip install -e .
```

## Requirements

- **Blender 3.0+** must be installed and in PATH
- Python 3.10+

### Install Blender

**macOS:**
```bash
brew install blender
```

**Ubuntu:**
```bash
sudo apt install blender
```

**Verify:**
```bash
blender --version
```

## Usage

### Interactive REPL Mode

```bash
blender-cli
# or just:
blender-cli repl
```

### Project Management

```bash
blender-cli project new my_scene --output ./projects
blender-cli project open ./projects/my_scene.blend
blender-cli project save
blender-cli project info
```

### Object Operations

```bash
blender-cli object add cube
blender-cli object add sphere --location 0,0,2 --scale 1,1,1
blender-cli object list
blender-cli object delete Cube
blender-cli object transform Cube --location 1,2,3 --rotation 0,0,45
```

### Rendering

```bash
blender-cli render image output.png --project scene.blend --frame 1 --resolution 1920x1080
```

### Export

```bash
blender-cli export gltf scene.glb --project scene.blend
blender-cli export fbx scene.fbx --project scene.blend
blender-cli export obj scene.obj --project scene.blend
```

### JSON Output

All commands support `--json` flag for machine-readable output:

```bash
blender-cli object list --json
```

## Architecture

```
cli_anything/blender/
├── blender_cli.py     # Main Click CLI + REPL
├── core/
│   ├── project.py     # Project lifecycle
│   ├── object.py      # Object manipulation
│   ├── render.py      # Render pipeline
│   ├── export.py       # Format export
│   └── session.py     # State management
└── utils/
    ├── blender_backend.py  # Blender subprocess wrapper
    └── repl_skin.py        # REPL UI
```

## Command Groups

| Group | Commands |
|-------|----------|
| `project` | new, open, save, info |
| `object` | add, list, delete, transform |
| `render` | image, animation |
| `export` | gltf, fbx, obj, usd |
| `session` | status, undo, redo |

## How It Works

1. **CLI parses commands** → Click dispatches to core modules
2. **Core modules build Python scripts** → bpy API calls
3. **Backend invokes Blender** → `blender --background --python script.py`
4. **Output returned as JSON** → Agent parses and continues

The CLI does NOT reimplement Blender. It wraps Blender's Python API and CLI interface.
