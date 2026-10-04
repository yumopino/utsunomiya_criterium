import bpy,bmesh,os
from mathutils import Vector
OUT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=OUT+'/utsunomiya_japan_cup_race.blend')
s=bpy.context.scene
for mesh in {o.data for o in bpy.data.collections['09 • Race riders — life-size'].objects}:
 bm=bmesh.new();bm.from_mesh(mesh);remaining=set(bm.verts)
 while remaining:
  seed=remaining.pop();group={seed};stack=[seed]
  while stack:
   v=stack.pop()
   for e in v.link_edges:
    w=e.other_vert(v)
    if w in remaining:remaining.remove(w);group.add(w);stack.append(w)
  center=sum((v.co for v in group),Vector())/len(group)
  if (center-Vector((-.115,0,1.49))).length<.02:bmesh.ops.delete(bm,geom=list(group),context='VERTS')
 bm.to_mesh(mesh);bm.free();mesh.update()
for o in s.objects:
 if o.name.startswith(('Checkered finish','Lane dash','Road edge')):o.location.z=.103;o.dimensions.z=.004
s.camera=bpy.data.objects['04 • Peloton at finish'];bpy.ops.wm.save_as_mainfile(filepath=OUT+'/utsunomiya_japan_cup_race.blend')
for camera,name in [('04 • Peloton at finish','race_peloton.png'),('05 • West hairpin riders','race_hairpin.png'),('06 • Rider detail','race_rider_detail.png')]:
 s.camera=bpy.data.objects[camera];s.render.filepath=OUT+'/'+name;bpy.ops.render.render(write_still=True)
print('REFINED',flush=True)
