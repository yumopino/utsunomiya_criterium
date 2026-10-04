import bpy, math, random, os, json
from mathutils import Vector
from math import pi, sin, cos
OUT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=OUT+'/utsunomiya_japan_cup_2026.blend')
random.seed(2026)
scene=bpy.context.scene
collection=bpy.data.collections.new('09 • Race riders — life-size');scene.collection.children.link(collection)
crowd=bpy.data.collections.new('10 • Spectators');scene.collection.children.link(crowd)
def mat(n,c,metal=0,rough=.5):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
black=mat('Race • carbon',(.015,.023,.032),.3,.3);rubber=mat('Race • tyre rubber',(.012,.013,.016));silver=mat('Race • alloy',(.5,.57,.62),.8,.24);skin=mat('Race • skin',(.58,.32,.19));white=mat('Race • helmet white',(.95,.95,.91));lens=mat('Race • mirrored glasses',(.02,.25,.38),.75,.16)
colors=[(.85,.025,.04),(.02,.25,.8),(.95,.65,.015),(.02,.48,.3),(.65,.025,.5),(.9,.9,.86)]
jerseys=[mat('Race • team %02d'%(i+1),c) for i,c in enumerate(colors)]
parts=[]
def reg(o,m):
 for c in list(o.users_collection):c.objects.unlink(o)
 collection.objects.link(o);o.data.materials.append(m);parts.append(o);return o
def rod(n,a,b,r,m):
 d=Vector(b)-Vector(a);bpy.ops.mesh.primitive_cylinder_add(vertices=10,radius=r,depth=d.length,location=(Vector(a)+Vector(b))/2);o=reg(bpy.context.object,m);o.name=n;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();return o
def ball(n,p,s,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=1,location=p);o=reg(bpy.context.object,m);o.name=n;o.scale=s;return o
# Forward +X. Axles along Y. Tyres sit on asphalt z=.10.
def hoop(n,p,r,t,m):
 bpy.ops.mesh.primitive_torus_add(major_segments=32,minor_segments=8,location=p,rotation=(pi/2,0,0),major_radius=r,minor_radius=t);o=reg(bpy.context.object,m);o.name=n;return o
prototypes=[]
for team in range(6):
 parts=[];kit=jerseys[team]
 rear=(-.53,0,.46);front=(.53,0,.46);bb=(-.13,0,.40);seat=(-.24,0,.98);head=(.36,0,.94)
 for wheel in [rear,front]:
  hoop('28 inch road tyre',wheel,.34,.025,rubber);hoop('Deep section rim',wheel,.302,.027,black)
  rod('Hub',(wheel[0],-.065,wheel[2]),(wheel[0],.065,wheel[2]),.035,silver)
  for k in range(12):
   a=2*pi*k/12;rod('Spoke',(wheel[0],0,wheel[2]),(wheel[0]+.29*cos(a),0,wheel[2]+.29*sin(a)),.004,silver)
 for a,b in [(bb,seat),(seat,head),(head,bb)]:rod('Carbon frame',a,b,.029,kit)
 for side in [-1,1]:
  r=(rear[0],side*.06,rear[2]);rod('Seat stay',seat,r,.012,kit);rod('Chain stay',bb,r,.016,kit);rod('Fork',(head[0],side*.055,head[2]),(front[0],side*.055,front[2]),.02,black)
 rod('Seatpost',seat,(-.26,0,1.075),.022,black);ball('Saddle',(-.26,0,1.075),(.14,.075,.03),black)
 rod('Stem',head,(.52,0,1.03),.023,black);rod('Handlebar',(.52,-.20,1.03),(.52,.20,1.03),.016,black)
 for y in [-.2,.2]:
  pts=[(.52,y,1.03),(.62,y,1.01),(.65,y,.93),(.6,y,.85),(.52,y,.85)]
  for a,b in zip(pts,pts[1:]):rod('Drop bar',a,b,.016,black)
 hoop('Chainring',(-.13,-.07,.4),.09,.008,silver)
 rod('Chain upper',(-.53,-.08,.49),(-.13,-.08,.49),.007,silver);rod('Chain lower',(-.53,-.08,.43),(-.13,-.08,.31),.007,silver)
 # Rider in racing tuck, feet remain coupled to the cranks.
 phase=team*pi/3
 pelvis=(-.22,0,1.10);shoulder=(.18,0,1.43)
 torso=ball('Jersey torso',(-.015,0,1.29),(.16,.17,.29),kit);torso.rotation_euler[1]=.83
 ball('Bib shorts',pelvis,(.18,.17,.16),black)
 for side in [-1,1]:
  y=side*.13;a=phase+(pi if side>0 else 0);foot=(-.13+.16*cos(a),y,.40+.16*sin(a));knee=(.06+ .08*cos(a),y,.80+.10*sin(a))
  hip=(-.22,side*.105,1.08);rod('Shorts thigh',hip,Vector(hip).lerp(Vector(knee),.55),.077,black);rod('Thigh',Vector(hip).lerp(Vector(knee),.48),knee,.061,skin);ball('Knee',knee,(.06,.06,.06),skin);rod('Shin',knee,foot,.043,skin);rod('Sock',Vector(knee).lerp(Vector(foot),.80),foot,.047,white);ball('Cycling shoe',(foot[0]+.035,y,foot[2]),(.105,.048,.035),white);rod('Crank',(-.13,y,.4),foot,.014,silver)
  sh=(.16,side*.15,1.43);el=(.30,side*.20,1.21);hand=(.54,side*.20,1.02)
  rod('Jersey sleeve',sh,Vector(sh).lerp(Vector(el),.5),.065,kit);rod('Upper arm',Vector(sh).lerp(Vector(el),.45),el,.045,skin);rod('Forearm',el,hand,.038,skin);ball('Glove',hand,(.045,.04,.05),black)
 rod('Neck',(.20,0,1.45),(.28,0,1.54),.06,skin);ball('Head',(.31,0,1.57),(.105,.087,.12),skin);ball('Helmet',(.29,0,1.66),(.145,.115,.075),kit);ball('Glasses',(.401,0,1.59),(.018,.09,.035),lens)
 for y in [-.055,0,.055]:rod('Helmet vent',(.21,y,1.71),(.35,y,1.70),.009,black)
 # White race-number patch on jersey back.
 # Number graphics omitted from schematic riders.
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.convert(target='MESH');bpy.ops.object.join();o=bpy.context.object;o.name='Rider prototype %02d'%(team+1)
 bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
 for p in o.data.polygons:p.use_smooth=True
 prototypes.append(o)
riders=[]
def rider(x,y,yaw,team,lean=0):
 p=prototypes[team%6];o=bpy.data.objects.new('Rider %03d • Team %d'%(len(riders)+1,team%6+1),p.data);collection.objects.link(o);o.location=(x,y,0);o.rotation_euler=(lean,0,yaw);o['team']=team%6+1;o['scale_note']='1.06 m wheelbase; approximately 1.75 m overall bike length';riders.append(o)
# Main bunch approaches westbound finish. Longitudinal separation >=2.6m.
for row in range(12):
 for col in range(3):
  rider(-65+row*2.9+(.3 if col%2 else 0),5.0+col*2.25+random.uniform(-.18,.18),pi,random.randrange(6))
# Three breakaway riders and a trailing pair.
for i in range(3):rider(-78-i*3.7,7.5+sin(i)*.6,pi,i)
for i in range(2):rider(-22+i*3.3,6.5+i*1.8,pi,i+3)
L=(2250-2*pi*8)/2;west=-L/2;east=L/2
for center,start in [(west,pi/2),(east,-pi/2)]:
 for i in range(7):
  a=start+.20+i*.39;r=8
  rider(center+r*cos(a),r*sin(a),a+pi/2,i+1,.28)
for p in prototypes:bpy.data.objects.remove(p,do_unlink=True)
# Crowd on sidewalks, behind barrier; restrained scale and shared meshes.
for i in range(70):
 x=-105+random.random()*100;y=random.choice([-1,1])*random.uniform(15,18)
 parts=[];kit=jerseys[i%6];ball('Spectator coat',(x,y,1.22),(.22,.15,.35),kit);ball('Spectator head',(x,y,1.73),(.12,.12,.15),skin)
 for side in [-1,1]:
  rod('Spectator leg',(x+side*.10,y,.96),(x+side*.13,y,.28),.065,black)
  rod('Cheering arm',(x+side*.20,y,1.42),(x+side*.35,y,1.8 if i%3==0 else 1.07),.045,skin)
 for o in parts:collection.objects.unlink(o);crowd.objects.link(o)
for o in scene.objects:
 if o.name.startswith(('Checkered finish','Lane dash','Road edge')):
  o.location.z=.103;o.dimensions.z=.004
# Hide schematic line and annotation overlays for race views.
for name in ['05 • Course line — 2250 m','07 • Map annotations']:
 bpy.data.collections[name].hide_render=True
camcol=bpy.data.collections['08 • Cameras and lighting']
def camera(n,loc,target,lens):
 d=bpy.data.cameras.new(n);o=bpy.data.objects.new(n,d);camcol.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.lens=lens;d.clip_end=5000;return o
hero=camera('04 • Peloton at finish',(-83,-10,7),(-51,6.5,1.05),44)
turn=camera('05 • West hairpin riders',(west-20,-17,8),(west-3,0,1),45)
detail=camera('06 • Rider detail',(-69,1,2.8),(-62,6.8,1.0),52)
scene.camera=hero;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True
scene.render.resolution_x=1600;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
scene['race_riders']='55 illustrative riders in six fictional team kits, road bikes at metric scale, racing tuck and banked hairpins. Static race scene.'
scene['race_riders_count']=len(riders)
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA'
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/utsunomiya_japan_cup_race.blend')
for cam,filename in [(hero,'race_peloton.png'),(turn,'race_hairpin.png'),(detail,'race_rider_detail.png')]:
 scene.camera=cam;scene.render.filepath=OUT+'/'+filename;bpy.ops.render.render(write_still=True)
with open(OUT+'/riders_validation.json','w') as f:json.dump({'riders':len(riders),'teams':6,'spectators':70,'bike_wheelbase_m':1.06,'scene':'utsunomiya_japan_cup_race.blend','static_scene':True},f,indent=2)
print('RACE_RIDERS_COMPLETE',len(riders),flush=True)
