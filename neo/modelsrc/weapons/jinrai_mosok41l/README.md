# v_jinrai_mosok41l with segmented reloads - research branch

Decompiled from the shipped viewmodel and recompiled with the M41 plan's partial, resume and draw-resume reload
sequences (`segments.csv`, rows `m41.*`, shared by the M41, M41S and M41L; frame counts resolved on the M41 and
reused, each model built from its own animations). After magazine seating, a partial reload is complete and
returns to idle. Dry resume uses the 37-frame direct-bolt clip (bolt grab f92; bolt event at 0.666 s), without
replaying the tap/slap. The tap remains part of an uninterrupted reload. Built with ntre's `proposals/0057-reload-cue-timing/tools/` (mdl2smd.py,
segments_build.py) and studiomdl (MDL v48).
