import bpy,os,math,json
from mathutils import Matrix
OUT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=OUT+'/utsunomiya_japan_cup_race.blend')
scene=bpy.context.scene
riders=list(bpy.data.collections['09 • Race riders — life-size'].objects)
meshes={o.data for o in riders}
for m in meshes:m.transform(Matrix.Rotation(math.pi/2,4,'X'));m.update()
scene.camera=bpy.data.objects['04 • Peloton at finish']
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/utsunomiya_japan_cup_race.blend')
for camera,name in [('04 • Peloton at finish','race_peloton.png'),('05 • West hairpin riders','race_hairpin.png'),('06 • Rider detail','race_rider_detail.png')]:
 scene.camera=bpy.data.objects[camera];scene.render.filepath=OUT+'/'+name;bpy.ops.render.render(write_still=True)
print('ORIENTATION_FIXED',len(riders),flush=True)
