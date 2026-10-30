"""Export saved Blender reload-phase projects with Blender Source Tools.

Run: blender --background --python-exit-code 1 --python export_reload_phases.py
Requires Blender 5.2 or newer and Blender Source Tools 3.4.3.
"""
from pathlib import Path
import sys

import bpy


def export_project(project):
    bpy.ops.wm.open_mainfile(filepath=str(project))
    bpy.ops.preferences.addon_enable(module="io_scene_valvesource")
    scene = bpy.context.scene
    folder = project.parent
    reference = folder / scene.get("reference_smd", "")
    if not reference.is_file():
        raise RuntimeError(f"Missing reference SMD for {project}: {reference}")
    reference_bytes = reference.read_bytes()
    armatures = [obj for obj in scene.objects if obj.type == "ARMATURE"]
    if len(armatures) != 1:
        raise RuntimeError(f"Expected one armature in {project}; found {len(armatures)}")
    armature = armatures[0]
    if armature.animation_data is None or armature.animation_data.action is None:
        raise RuntimeError(f"No animation action in {project}")
    expected = [
        folder / "anims" / (slot.name_display + ".smd")
        for slot in armature.animation_data.action.slots
    ]
    previous = {
        path: path.stat().st_mtime_ns if path.exists() else None
        for path in expected
    }

    scene.vs.export_path = "//"
    scene.vs.export_format = "SMD"
    armature.data.vs.action_selection = "FILTERED"
    armature.vs.action_filter = "*"
    armature.vs.subdir = "anims"
    armature.vs.export = True
    for obj in scene.objects:
        if obj.type == "MESH":
            obj.vs.export = False
    for collection in bpy.data.collections:
        collection.vs.export = False

    result = bpy.ops.export_scene.smd(export_scene=True)
    if result != {"FINISHED"}:
        raise RuntimeError(f"Source Tools export failed for {project}: {result}")
    missing = [path for path in expected if not path.is_file()]
    stale = [
        path for path in expected
        if path.is_file() and path.stat().st_mtime_ns == previous[path]
    ]
    if missing or stale:
        raise RuntimeError(
            f"Incomplete export for {project}; missing={missing}, unchanged={stale}"
        )
    if reference.read_bytes() != reference_bytes:
        raise RuntimeError(f"Reference mesh changed during export: {reference}")
    print(f"EXPORTED {project.name}: {len(expected)} animations; reference retained", flush=True)


def main():
    root = Path(__file__).resolve().parent
    filters = set(sys.argv[sys.argv.index("--") + 1:]) if "--" in sys.argv else set()
    projects = sorted(root.glob("*/*.blend"))
    if filters:
        projects = [path for path in projects if path.parent.name in filters]
    if not projects:
        raise RuntimeError("No matching Blender projects found")
    for project in projects:
        export_project(project)


if __name__ == "__main__":
    main()
