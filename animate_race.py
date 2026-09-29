import bpy, math, os, json, bisect, time
from mathutils import Vector
OUT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(OUT,'utsunomiya_japan_cup_2026.blend'))
scene=bpy.context.scene
for o in bpy.data.collections['05 • Course line — 2250 m'].objects: o.hide_render=True
curve=next(o for o in scene.objects if o.type=='CURVE' and o.name.startswith('Official course'))
points=[Vector(p.co[:3]) for p in curve.data.splines[0].points]
segments=[]; ends=[]; total=0
for a,b in zip(points,points[1:]+points[:1]):
 length=(b-a).length
 if length>1e-8: segments.append((total,length,a,b)); total+=length; ends.append(total)
start=points[0].x+58
L=(2250-2*math.pi*8)/2
centers=[L+math.pi*8/2,2*L+3*math.pi*8/2]
def speed(s,cruise):
 d=min(min(abs(s%total-c),total-abs(s%total-c)) for c in centers)
 u=max(0,min(1,(d-math.pi*8/2)/65))
 return 5+(cruise-5)*u*u*(3-2*u)
ds=.25
steps=math.ceil(total/ds); ds=total/steps
travel=[i*ds for i in range(steps+1)]
def timetable(cruise):
 times=[0.]
 for d in travel[1:]: times.append(times[-1]+ds/speed(start+d-ds/2,cruise))
 return times
lo=50/3.6; hi=90/3.6
for _ in range(40):
 mid=(lo+hi)/2
 if timetable(mid)[-1]>162: lo=mid
 else: hi=mid
cruise=(lo+hi)/2; times=timetable(cruise)
def position(s):
 s%=total; i=min(bisect.bisect_left(ends,s),len(segments)-1); off,length,a,b=segments[i]; return a.lerp(b,(s-off)/length)
camdata=bpy.data.cameras.new('Race POV 20mm'); cam=bpy.data.objects.new('Race POV — average 50 kmh',camdata); scene.collection.objects.link(cam)
camdata.lens=20; camdata.clip_start=.05;camdata.clip_end=2000;cam.rotation_mode='QUATERNION';scene.camera=cam
fps=24; count=162*fps
values=[[] for _ in range(7)]; previous=None
for frame in range(1,count+1):
 t=(frame-1)/(count-1)*162; idx=max(1,min(bisect.bisect_left(times,t),steps)); d=travel[idx-1]+ds*(t-times[idx-1])/(times[idx]-times[idx-1]); s=start+d
 pos=position(s);pos.z=1.65; target=position(s+4);target.z=1.6
 q=(target-pos).to_track_quat('-Z','Y')
 if previous is not None and previous.dot(q)<0:q.negate()
 previous=q.copy()
 for arr,val in zip(values,list(pos)+list(q)): arr.extend([frame,val])
cam.animation_data_create(); action=bpy.data.actions.new('162 second race lap');cam.animation_data.action=action
for i,arr in enumerate(values):
 fc=action.fcurves.new(data_path='location' if i<3 else 'rotation_quaternion',index=i if i<3 else i-3);fc.keyframe_points.add(count);fc.keyframe_points.foreach_set('co',arr)
 for kp in fc.keyframe_points:kp.interpolation='LINEAR'
scene.frame_start=1;scene.frame_end=count;scene.render.fps=fps;scene.render.fps_base=1
scene.render.engine='BLENDER_WORKBENCH'
sh=scene.display.shading;sh.light='STUDIO';sh.color_type='MATERIAL';sh.show_shadows=True;sh.show_cavity=True;sh.cavity_type='BOTH';sh.curvature_ridge_factor=1.15;sh.curvature_valley_factor=1.05;sh.show_specular_highlight=True;sh.background_type='WORLD';scene.world.color=(.33,.48,.65)
scene.display.render_aa='8';scene.view_settings.view_transform='Standard'
scene.render.resolution_x=1280;scene.render.resolution_y=720;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='FFMPEG';scene.render.ffmpeg.format='MPEG4';scene.render.ffmpeg.codec='H264';scene.render.ffmpeg.constant_rate_factor='HIGH';scene.render.ffmpeg.audio_codec='NONE';scene.render.filepath=OUT+'/utsunomiya_race_pov_50kmh.mp4'
scene['speed_profile']='Average 50 km/h, 18 km/h hairpins, smooth acceleration/braking. Illustrative racing speed, not measured telemetry.'
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/utsunomiya_race_pov_50kmh.blend')
with open(OUT+'/race_video_validation.json','w') as f:json.dump({'frames':count,'fps':fps,'duration_seconds':162,'average_kmh':total/162*3.6,'cruise_kmh':cruise*3.6,'hairpin_kmh':18,'eye_height_m':1.65,'lap_m':total,'resolution':[1280,720],'note':'Designed speed profile, not actual race telemetry.'},f,indent=2)
scene.render.image_settings.file_format='PNG';scene.render.filepath=OUT+'/race_pov_preview.png';bpy.ops.render.render(write_still=True)
if os.environ.get('RACE_PREVIEW_ONLY')!='1':
 scene.render.image_settings.file_format='FFMPEG';scene.render.ffmpeg.format='MPEG4';scene.render.ffmpeg.codec='H264';scene.render.ffmpeg.constant_rate_factor='HIGH';scene.render.filepath=OUT+'/utsunomiya_race_pov_50kmh.mp4';bpy.ops.render.render(animation=True)
 import glob
 for p in glob.glob(OUT+'/utsunomiya_race_pov_50kmh.mp4*.mp4'):os.replace(p,OUT+'/utsunomiya_race_pov_50kmh.mp4')
 print('RACE_VIDEO_COMPLETE',flush=True)
