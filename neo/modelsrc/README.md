# Models and Animations

## Tools

* Use Blender 5.2.3 or newer. The files are tested with Blender 5.2.3.
* Use Blender Source Tools 3.4.3 or newer to export SMD files from Blender. Get it from
  steamreview.org/BlenderSourceTools. To install it, see Setup in [weapons/README.md](weapons/README.md).
* Use Python 3 to run the optional compile helper scripts. Export helper scripts run inside Blender, which includes `bpy`.
* Source SDK Base 2013 Multiplayer's `studiomdl.exe` compiles Source models. It is a Steam tool; see Compiling models
  in [weapons/README.md](weapons/README.md).

## Weapon viewmodels

For the viewmodels in `weapons/viewmodels.blend`, follow [weapons/README.md](weapons/README.md). It has the steps to
set up the tools (Windows included), change an animation, export, compile, and see the model in game.

Export the viewmodels with the script (`export_viewmodels.py`, or **Export gun** in the Viewmodel panel), not with
the plain Scene Export below. Only the script does these steps:

* It checks the range-of-motion limits of the rigs and stops when a key is outside a limit.
* It keeps the shipped clips unchanged and stops when one would change.

## Exporting other animations

For a model that has no export script: in Blender, open Scene Properties > Source Engine Export and set these
options:

* Set **Export Path** to `//` to write beside the Blender project.
* Set **Export Format** to SMD.
* Set **Engine Path** to the local `studiomdl.exe` location in Source SDK Base 2013 Multiplayer. (e.g. `C:\Program Files (x86)\Steam\steamapps\common\Source SDK Base 2013 Multiplayer\bin\`)
* Set the armature's **Action Selection** to **Slot Filter** to export every animation slot.
  The default first option, **Current Action Slot**, exports only the selected slot.
* For animation-only changes, leave mesh export disabled.

Then click **Export** in that panel and pick **Scene export**.

Note: Model and animation round trips can cause small floating-point and compiler compression differences.
