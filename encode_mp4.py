import bpy,os,glob
out=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene
s.sequence_editor_create().sequences.new_movie('Ride',glob.glob(out+'/*.mkv')[0],channel=1,frame_start=1)
s.frame_start=1;s.frame_end=72;s.render.fps=24;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.constant_rate_factor='HIGH';s.render.filepath=out+'/ride_final';s.render.use_file_extension=True
bpy.ops.render.render(animation=True)
p=glob.glob(out+'/ride_final*.mp4')[0];os.replace(p,out+'/utsunomiya_cyclist_pov_3s.mp4')
