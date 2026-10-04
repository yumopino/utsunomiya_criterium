# Race scene

Open `utsunomiya_japan_cup_race.blend` in Blender. The active camera shows the peloton approaching the finish. This is a static, illustrative race scene built on the original schematic circuit, not a reconstruction of a particular real race.

- 55 cyclists with metric-scale road bicycles, six fictional team colour schemes.
- 36 riders in the main bunch, three leaders, two trailing riders and seven riders at each hairpin.
- Road-bike wheelbase: 1.06 m; tyres, deep rims, spokes, frame triangles, fork, saddle, cranks, chain and drop handlebars.
- Riders have racing-tuck poses, helmets, glasses, gloves, shoes and alternating pedal poses. Hairpin riders lean into the turn.
- 70 spectators stand behind the roadside barriers.
- Camera 04: finish peloton; camera 05: west hairpin; camera 06: cyclist detail. Original course cameras remain available.
- Original course and exported videos remain separate. This file does not add animated pedalling or change existing videos.

Rebuild with Blender 4.3 using `add_race_riders.py`. The script saves the blend and renders `race_peloton.png`, `race_hairpin.png` and `race_rider_detail.png`. Road markings from the explanatory route overlay are hidden for race renders. Buildings and road geometry retain the original schematic assumptions.
