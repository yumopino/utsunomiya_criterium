import bpy, math, random, os, json
from mathutils import Vector
from math import pi, sin, cos
OUT=os.path.dirname(os.path.abspath(__file__))
random.seed(26)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
 if c.name!='Collection': bpy.data.collections.remove(c)
base=bpy.data.collections.get('Collection'); base.name='00 • Presentation'
def coll(name):
 c=bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c); return c
roads=coll('01 • Odori road and crossings'); city=coll('02 • Illustrative city blocks'); landmarks=coll('03 • Banba and Futaarayama'); race=coll('04 • Race infrastructure'); route=coll('05 • Course line — 2250 m'); plants=coll('06 • Trees and street furniture'); labels=coll('07 • Map annotations'); cams=coll('08 • Cameras and lighting')
def mat(n,c,metal=0):
 m=bpy.data.materials.new(n); m.diffuse_color=(*c,1); m.use_nodes=True; p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'); p.inputs['Base Color'].default_value=(*c,1); p.inputs['Roughness'].default_value=.72; p.inputs['Metallic'].default_value=metal; return m
navy=mat('Midnight blue',(.025,.065,.11)); road=mat('Asphalt',(.095,.125,.16)); pavement=mat('Warm concrete',(.64,.68,.66)); white=mat('Ivory paint',(.94,.95,.88)); red=mat('Course vermilion',(.9,.045,.028)); gold=mat('Accent ochre',(1,.57,.075)); glass=mat('Blue grey glazing',(.16,.31,.39),.35); dark=mat('Roof graphite',(.09,.15,.19)); wood=mat('Torii cedar',(.56,.24,.055)); green=mat('Tree leaves',(.15,.36,.25)); green2=mat('Tree leaves light',(.28,.48,.30)); grass=mat('Shrine hill',(.28,.39,.28)); pale=mat('Architectural light',(.77,.79,.73)); blue=mat('Architectural blue',(.42,.57,.64)); sand=mat('Architectural sand',(.66,.55,.41)); pink=mat('Architectural brick',(.54,.36,.30))
def link(o,c):
 for old in list(o.users_collection): old.objects.unlink(o)
 c.objects.link(o); return o
def box(n,loc,scale,m,c,bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=n; o.dimensions=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(m); link(o,c)
 if bevel:
  mod=o.modifiers.new('Soft edges','BEVEL'); mod.width=bevel; mod.segments=2; o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
 return o
def line(n,points,width,m,c,cyclic=False):
 cu=bpy.data.curves.new(n,'CURVE'); cu.dimensions='3D'; cu.resolution_u=1; cu.bevel_depth=width; cu.bevel_resolution=2; s=cu.splines.new('POLY'); s.points.add(len(points)-1)
 for p,co in zip(s.points,points): p.co=(*co,1)
 s.use_cyclic_u=cyclic; o=bpy.data.objects.new(n,cu); c.objects.link(o); o.data.materials.append(m); return o
def cyl(n,a,b,r,m,c,vertices=10):
 d=Vector(b)-Vector(a); bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=d.length,location=(Vector(a)+Vector(b))/2); o=bpy.context.object; o.name=n; o.rotation_euler=d.to_track_quat('Z','Y').to_euler(); o.data.materials.append(m); link(o,c); return o
fontpath='/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc'
font=bpy.data.fonts.load(fontpath) if os.path.exists(fontpath) else None
def txt(n,s,loc,size,m,c=labels,flat=True):
 cu=bpy.data.curves.new(n,'FONT'); cu.body=s; cu.size=size; cu.extrude=.015; cu.align_x='CENTER'; cu.space_character=1.1
 if font: cu.font=font
 o=bpy.data.objects.new(n,cu); c.objects.link(o); o.location=loc; o.data.materials.append(m)
 if not flat: o.rotation_euler=(pi/2,0,0)
 return o
# Schematic metric model. X east, Y north; route length matches official lap.
r=8; L=(2250-2*pi*r)/2; west=-L/2; east=L/2; finish=-58
box('Exhibition plinth',(0,0,-5),(1250,360,10),navy,base,4)
box('City ground',(0,23,-.6),(1200,230,1),pavement,roads)
box('Odori carriageway',(0,0,0),(1190,27,.2),road,roads)
for y in [-17,17]: box('Continuous sidewalk',(0,y,.22),(1190,7,.45),pavement,roads)
streets=[west-15,-355,-218,2,205,405,east+15]
for x in streets:
 box('Connecting street',(x,20,.03),(15,222,.22),road,roads)
 for sy in [-1,1]:
  for i in range(8): box('Zebra crossing',(x-6+i*1.7,sy*19,.2),(.85,8,.08),white,roads)
for x in range(-580,581,12):
 for y in [-4,4]: box('Lane dash',(x,y,.16),(5,.16,.035),white,roads)
for y in [-12,12]: box('Road edge',(0,y,.16),(1175,.2,.035),white,roads)
# Central safety divider ends before the two U turns.
box('Median',(0,0,.27),(L-24,1.3,.45),pale,race)
for x in range(-530,531,9):
 box('Median fence panel',(x,0,1.05),(8,.18,1.2),navy,race)
# North lane westbound, south lane eastbound, as official map.
pts=[(east-2*i*east/220,r,.35) for i in range(221)]
pts += [(west+r*cos(pi/2+pi*i/60),r*sin(pi/2+pi*i/60),.35) for i in range(1,61)]
pts += [(west+L*i/220,-r,.35) for i in range(1,221)]
pts += [(east+r*cos(-pi/2+pi*i/60),r*sin(-pi/2+pi*i/60),.35) for i in range(1,61)]
p=line('Official course • schematic racing line',pts,.5,red,route,True); p['official_lap_m']=2250; p['geometry_note']='Idealized straight corridor. U-turn radius assumed 8m. Not surveyed.'
for x in range(-475,500,95):
 for y,d in [(8,-1),(-8,1)]: line('Direction chevron',[(x-3*d,y-1.6,.48),(x,y,.48),(x-3*d,y+1.6,.48)],.33,gold,route)
# Stylized streetscape with independent editable buildings.
def building(n,x,y,w,d,h,m):
 box(n,(x,y,h/2+.3),(w,d,h),m,city,.45)
 box(n+' parapet',(x,y,h+.6),(w+.8,d+.8,1),pale,city)
 front=y-d/2-.08 if y>0 else y+d/2+.08
 for z in range(5,int(h)-1,5):
  box(n+' window band',(x,front,z),(w-3,.12,2.5),glass,city)
  for xx in range(int(x-w/2+4),int(x+w/2-1),5): box('Window mullion',(xx,front,z),(.25,.21,2.5),m,city)
 box(n+' storefront',(x,front,2),(w-2,.16,3),glass,city)
 box(n+' awning',(x,front+(-1 if y>0 else 1),4),(w-1,2,.25),random.choice([navy,red,sand]),city)
 box(n+' rooftop plant',(x+w*.18,y,h+1.8),(w*.22,d*.3,2),dark,city)
for side in [-1,1]:
 x=-580
 while x<580:
  w=random.uniform(17,32); cx=x+w/2
  if all(abs(cx-s)>w/2+11 for s in streets) and not (side==1 and -165<cx<20) and not(side==-1 and -138<cx<-40):
   building('Odori block %s %04d'%(side,cx+600),cx,side*random.uniform(37,44),w,random.uniform(22,33),random.uniform(14,38),random.choice([pale,blue,sand,pink]))
  x+=w+4
# Landmark masses interpreted from official diagram, no facade survey.
building('City Tower Utsunomiya • indicative',-144,46,29,33,87,blue)
building('Omotesando Square • indicative',-22,44,34,36,39,pale)
building('MEGA Don Quijote • indicative',-91,-45,62,37,26,sand)
building('Hotel New Itaya • indicative',463,-59,40,42,49,pink)
box('Banba plaza',(-70,47,.35),(68,55,.6),pale,landmarks)
box('Shrine green precinct',(-73,104,3),(115,66,6),grass,landmarks,5)
for i in range(22): box('Shrine approach stair',(-70,64+i*1.6,.6+i*.24),(16,1.65,.4+i*.48),pavement,landmarks)
for x in [-79,-61]: cyl('Cedar torii pillar',(x,40,.5),(x,40,13),.65,wood,landmarks,16)
box('Torii tie beam',(-70,40,10),(22,1.1,1.1),wood,landmarks)
line('Torii curved lintel',[(-84,40,13.8),(-79,40,13.2),(-70,40,13),(-61,40,13.2),(-56,40,13.8)],.7,dark,landmarks)
box('Torii upper cedar',(-70,40,12.5),(27,1.3,.65),wood,landmarks)
box('Shrine main hall',(-70,113,11),(24,17,13),wood,landmarks)
# Japanese gable roof prism.
verts=[(-86,101,17),(-54,101,17),(-70,101,25),(-86,125,17),(-54,125,17),(-70,125,25)]
me=bpy.data.meshes.new('Shrine roof'); me.from_pydata(verts,[],[(0,1,2),(3,5,4),(0,3,4,1),(0,2,5,3),(1,4,5,2)]); me.update(); o=bpy.data.objects.new('Futaarayama shrine • illustrative roof',me); landmarks.objects.link(o); me.materials.append(dark)
def tree(x,y,z=0):
 cyl('Street tree trunk',(x,y,z),(x,y,z+4),.35,wood,plants)
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=3.5,location=(x,y,z+6)); o=bpy.context.object; o.name='Tree canopy'; o.scale=(1,1,1.3); o.data.materials.append(random.choice([green,green2])); link(o,plants)
for x in range(-570,580,27):
 if all(abs(x-s)>12 for s in streets):
  for y in [-20,21]:
   if not(-93<x<-45 and y>0): tree(x,y)
for i in range(36):
 x=random.uniform(-124,-22); y=random.uniform(83,131)
 if abs(x+70)>19: tree(x,y,6)
# Event furniture.
for x in range(-536,537,8):
 for y in [-13.2,13.2]:
  box('Race barrier',(x,y,.9),(7.6,.2,1.5),random.choice([pale,pale,navy]),race)
for x in [finish-1]:
 for y in [-14,14]: box('Finish gantry pier',(x,y,5),(1.2,1.2,10),navy,race)
 box('Finish gantry header',(x,0,10),(1.5,29,2),red,race)
 # Text faces down the boulevard.
 t=txt('Finish banner','JAPAN CUP',(x-.8,0,9.8),1.35,white,race,False); t.rotation_euler=(pi/2,0,-pi/2)
for i in range(24):
 for j in range(2): box('Checkered finish',(finish+j*.55,-12+i+.5,.22),(.55,1,.06),white if (i+j)%2 else dark,race)
for x in [-110,-96,-82,-68]:
 box('Hospitality tent',(x,-73,2.5),(10,8,5),white,race)
 bpy.ops.mesh.primitive_cone_add(vertices=4,radius1=7.6,radius2=0,depth=3,rotation=(0,0,pi/4),location=(x,-73,6.5)); o=bpy.context.object; o.data.materials.append(red); link(o,race)
for x in range(-500,520,65):
 for y in [-21,21]:
  cyl('Streetlight mast',(x,y,0),(x,y,9),.13,dark,plants)
  box('Streetlight head',(x,y,9),(3,.8,.3),gold,plants)
# Clean diagram labels, on the plinth.
txt('Title','UTSUNOMIYA  /  JAPAN CUP',(0,-143,.1),24,white)
txt('Subtitle','CRITERIUM     •     ODORI CIRCUIT     /     2.25 KM',(0,-165,.1),10,gold)
for x,number,name in [(west,'02','TOBU BASHAMICHI'),(finish,'01','BANBA  /  START + FINISH'),(east,'03','KAMIGAWARA')]:
 line('Callout leader',[(x,0,1),(x,-87,1)],.35,gold,labels)
 txt('Course marker '+number,number,(x,-109,1),17,gold)
 txt('Location '+name,name,(x,-122,1),6,white)
txt('Shrine label','FUTAARAYAMA SHRINE',(-70,143,1),7,white)
txt('Scale note','SCHEMATIC CITY MODEL  •  2026 OFFICIAL ROUTE',(315,143,1),6,pale)
line('100 metre scale',[(320,119,1),(420,119,1)],.5,white,labels)
for x in [320,420]: line('Scale tick',[(x,116,1),(x,122,1)],.5,white,labels)
txt('Scale caption','100 m',(370,126,1),6,white)
line('North arrow',[(-565,106,1),(-565,140,1),(-570,131,1),(-565,140,1),(-560,131,1)],.6,gold,labels); txt('North','N',(-565,148,1),8,white)
# Cameras.
def camera(n,loc,target,scale):
 bpy.ops.object.camera_add(location=loc); o=bpy.context.object; o.name=n; link(o,cams); o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler(); o.data.type='ORTHO'; o.data.ortho_scale=scale; o.data.clip_end=5000; return o
hero=camera('01 • Entire course',(100,-850,1050),(0,0,0),1330)
close=camera('02 • Banba square',(-215,-235,180),(-66,24,10),310)
top=camera('03 • Plan',(0,0,1400),(0,0,0),1300)
scene=bpy.context.scene; scene.unit_settings.system='METRIC'; scene.camera=hero
scene.render.engine='CYCLES'; scene.cycles.samples=24; scene.cycles.use_denoising=True
scene.world.color=(.3,.3,.3)
bpy.ops.object.light_add(type='AREA',location=(0,-200,700)); light=bpy.context.object; light.name='Large softbox'; light.data.energy=6000000; light.data.shape='DISK'; light.data.size=850; link(light,cams)
bpy.ops.object.light_add(type='SUN',location=(0,0,500)); light=bpy.context.object; light.rotation_euler=(.4,-.5,-.3); light.data.energy=2; light.data.angle=.25; link(light,cams)
scene.view_settings.view_transform='AgX'; scene.render.resolution_x=2200; scene.render.resolution_y=1100; scene.render.resolution_percentage=100
scene['source']='https://www.japancup.gr.jp/y2026/criterium/'
scene['accuracy']='Conceptual model from official diagram; buildings, widths, elevations and positions approximate. Route idealized to 2250m.'
scene['axis']='X east / Y north / Z up. Units metres.'
# Make Blender open directly to a useful overview.
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.region_3d.view_perspective='CAMERA'; area.spaces.active.clip_end=5000
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'utsunomiya_japan_cup_2026.blend'))
scene.render.filepath=os.path.join(OUT,'course_overview.png'); bpy.ops.render.render(write_still=True)
scene.camera=close; scene.render.resolution_x=1600; scene.render.resolution_y=1200; scene.render.filepath=os.path.join(OUT,'banba_detail.png'); bpy.ops.render.render(write_still=True)
scene.camera=hero
length=sum((Vector(pts[(i+1)%len(pts)])-Vector(pts[i])).length for i in range(len(pts)))
with open(os.path.join(OUT,'validation.json'),'w') as f: json.dump({'route_length_m':length,'official_lap_m':2250,'objects':len(scene.objects),'cameras':[hero.name,close.name,top.name],'assumptions':'Schematic road geometry; illustrative buildings, road widths and levels.'},f,indent=2)
print('COURSE_COMPLETE',length)
