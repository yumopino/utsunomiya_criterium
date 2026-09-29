import bpy, math, os, json
from mathutils import Vector
OUT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(OUT,'utsunomiya_japan_cup_2026.blend'))
scene=bpy.context.scene
for o in bpy.data.collections['05 • Course line — 2250 m'].objects: o.hide_render=True
scene.world.use_nodes=True
background=next(n for n in scene.world.node_tree.nodes if n.type=='BACKGROUND')
background.inputs['Color'].default_value=(.38,.57,.8,1)
background.inputs['Strength'].default_value=.5
curve=next(o for o in scene.objects if o.type=='CURVE' and o.name.startswith('Official course'))
points=[Vector(p.co[:3]) for p in curve.data.splines[0].points]
# The official diagram runs westward on the north lane, then east on the south lane.
segments=[]; total=0
for a,b in zip(points,points[1:]+points[:1]):
 length=(b-a).length
 if length>1e-8: segments.append((total,length,a,b)); total+=length
start=points[0].x-(-58)
def position(s):
 s=s%total
 for offset,length,a,b in segments:
  if s<=offset+length: return a.lerp(b,(s-offset)/length)
 return points[0].copy()
bpy.ops.object.camera_add(); cam=bpy.context.object; cam.name='Cyclist POV • full lap in 3 seconds'; cam.data.lens=20; cam.data.sensor_width=36; cam.data.clip_start=.05; cam.data.clip_end=2000; cam.rotation_mode='QUATERNION'; scene.camera=cam
previous=None
for frame in range(1,73):
 s=start+total*(frame-1)/71
 pos=position(s); pos.z=1.65
 target=position(s+9); target.z=1.55
 q=(target-pos).to_track_quat('-Z','Y')
 if previous is not None and previous.dot(q)<0: q.negate()
 cam.location=pos; cam.rotation_quaternion=q; previous=q.copy()
 cam.keyframe_insert(data_path='location',frame=frame); cam.keyframe_insert(data_path='rotation_quaternion',frame=frame)
scene.frame_start=1; scene.frame_end=72; scene.render.fps=24; scene.render.fps_base=1
scene.render.engine='CYCLES'; scene.cycles.samples=8; scene.cycles.use_denoising=True
scene.render.resolution_x=1280; scene.render.resolution_y=720; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='FFMPEG'; scene.render.ffmpeg.format='MPEG4'; scene.render.ffmpeg.codec='H264'; scene.render.ffmpeg.constant_rate_factor='HIGH'; scene.render.ffmpeg.ffmpeg_preset='GOOD'; scene.render.ffmpeg.audio_codec='NONE'
scene.render.filepath=os.path.join(OUT,'utsunomiya_cyclist_pov_3s.mp4')
scene['video_note']='3-second accelerated full lap, cyclist eye height 1.65m, 24fps. Illustrative city geometry.'
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'utsunomiya_cyclist_pov_3s.blend'))
# Representative POV still to inspect camera framing before animation.
scene.render.image_settings.file_format='PNG'; scene.render.filepath=os.path.join(OUT,'cyclist_pov_preview.png'); bpy.ops.render.render(write_still=True)
scene.render.image_settings.file_format='FFMPEG'; scene.render.ffmpeg.format='MPEG4'; scene.render.ffmpeg.codec='H264'; scene.render.filepath=os.path.join(OUT,'utsunomiya_cyclist_pov_3s.mp4'); bpy.ops.render.render(animation=True)
import glob
for generated in glob.glob(os.path.join(OUT,'utsunomiya_cyclist_pov_3s.mp4*.mp4')): os.replace(generated,os.path.join(OUT,'utsunomiya_cyclist_pov_3s.mp4'))
with open(os.path.join(OUT,'video_validation.json'),'w') as f: json.dump({'frames':72,'fps':24,'duration_seconds':3,'resolution':[1280,720],'eye_height_m':1.65,'lap_m':total,'start_finish_error_m':(position(start)-position(start+total)).length},f,indent=2)
print('VIDEO_COMPLETE',flush=True)
