# Research reload-phase animation projects

The folders in this directory contain editable Blender projects for the reload
phase work on `research-reload-phases`. Each project is the source for its
folder's `anims/*.smd` exports. Keep the `.blend`, its reference SMD, the QC,
and the animation exports together.

There are 37 animation projects and 42 QCs. Most folders contain one model and
one project named after its QC. The MX, MX-S, and ZR68 folders share an
animation set across their team QCs, so each has one project named
`<folder>_reload_phases.blend`. Its reference mesh is for preview; the team
references have matching bone hierarchies. Those shared projects preview the
first QC's Jinrai reference; each QC still compiles its own team-specific
reference mesh, sequence metadata, activities, and events.

## Requirements and editing

- Blender 5.2 or newer; the projects were created with Blender 5.2.3.
- Blender Source Tools 3.4.3, enabled in Blender preferences.
- Source SDK Base 2013 Multiplayer's `bin/studiomdl.exe` for compilation.
- Python 3 for the compile helper; no extra packages are required.

Open the `.blend` in the relevant model folder and edit its animation slots.
The `anims/*.smd` files are generated exports, not the editing source.
`segments.csv` and each folder's README retain research timing and provenance;
they are not used to export or compile the saved Blender projects.

The preview mesh and camera are for animation inspection. Blender Source Tools
does not export the mesh in these projects: keep the existing reference SMD
unchanged. The preview uses imported material names without decoded texture
images.

## Export animations

From this directory, export every saved project with:

```sh
blender --background --python-exit-code 1 --python export_reload_phases.py
```

The helper exports every animation slot to its folder's `anims/` directory,
checks that all expected files were freshly written, and verifies that the
reference SMD was not changed. To export selected folder names only, append
them after `--`, for example `-- jinrai_tachi mx`.

The project exporter leaves QC files unchanged. Edit the matching QC as well
if a sequence's name, activity, playback rate, transition, or event changes.

## Compile models

Compile all 42 QCs into a separate directory:

```sh
python compile_reload_phases.py --compiler "C:/path/to/studiomdl.exe" --output "C:/path/to/output/models/weapons"
```

The helper compiles in a temporary game configuration and copies only the
resulting model files to `--output`; it does not edit a game's `gameinfo.txt`.
To update the compiled assets in neoAssets, use
`--output "../../models/weapons"` from this directory, then review the
binary diff before including it.

The local SDK rebuild was not byte-identical to the committed models.
Semantic checks found the same bones, sequences, frame counts, FPS, and vertex
positions across all 42 models; the largest decoded bone rotation difference
was 0.09 degrees. Keep the existing compiled assets unless a rebuild is
deliberate.

The compiled model folder is `neo/models/weapons/`. A game install is not
required to export or compile. Any animation or QC change still needs an
in-game check before it is treated as behavior-preserving.
