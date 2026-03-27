# Blender CLI Test Plan

## Test Inventory

- `test_core.py`: ~10 unit tests planned
- `test_full_e2e.py`: ~5 E2E tests planned

## Unit Test Plan

### test_core.py

**Module: project.py**
- `test_create_project`: Create project with valid name → verify state file created
- `test_create_project_invalid_dir`: Create project in non-existent dir → error
- `test_open_project`: Open existing .blend → verify state returned
- `test_open_project_not_found`: Open non-existent file → error
- `test_project_info`: Get info for open project → verify structure

**Module: object.py**
- `test_add_object_valid_types`: Add cube/sphere/plane → verify return structure
- `test_add_object_invalid_type`: Add invalid type → error or graceful handling
- `test_list_objects`: List objects in new scene → verify empty list
- `test_transform_object`: Transform cube → verify state update

**Module: session.py**
- `test_session_initial_state`: New session has default values
- `test_session_undo_redo`: Push state, undo, redo → verify behavior

## E2E Test Plan

**test_full_e2e.py**

- `test_render_image_real_blender`: Render a real .blend → verify PNG created with valid header
- `test_export_gltf_real_blender`: Export to glTF → verify .glb file created with valid glTF magic bytes
- `test_export_fbx_real_blender`: Export to FBX → verify .fbx file created
- `test_object_add_render_cycle`: Add object → render → verify output

## Realistic Workflow Scenarios

**Workflow 1: Basic 3D Scene Creation**
- Operations: `project new` → `object add cube` → `object add sphere` → `render image`
- Verified: Output PNG exists, file size > 0

**Workflow 2: glTF Export Pipeline**
- Operations: `project new` → `object add` (multiple) → `export gltf`
- Verified: .glb file valid (glTF magic bytes)

**Workflow 3: Object Manipulation**
- Operations: `object add` → `object transform` → `object list` → `render`
- Verified: Transformed object visible in render output
