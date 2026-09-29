import bpy,os,glob,json
OUT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene; editor=s.sequence_editor_create();fps=24
clips=[('01 / BANBA START',0,4),('02 / ODORI AVENUE',18,4),('03 / WEST HAIRPIN',34.8,6),('04 / ODORI STRAIGHT',75,5),('05 / EAST HAIRPIN',115,6),('06 / FINISH',157,5)]
frame=1;meta=[]
for index,(label,start,duration) in enumerate(clips):
 length=round(duration*fps);offset=round(start*fps)
 strip=editor.sequences.new_movie(label,OUT+'/utsunomiya_race_pov_50kmh.mp4',channel=1,frame_start=frame-offset)
 strip.frame_final_start=frame;strip.frame_final_end=frame+length
 title=editor.sequences.new_effect(label+' title',type='TEXT',channel=2,frame_start=frame,frame_end=frame+length)
 title.text=label;title.font_size=25;title.color=(1,1,1,1);title.location=(.5,.9);title.use_shadow=True
 meta.append({'label':label,'source_start_seconds':start,'duration_seconds':duration,'timeline_start':frame})
 frame+=length
s.frame_start=1;s.frame_end=frame-1;s.render.fps=fps;s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.constant_rate_factor='NONE';s.render.ffmpeg.video_bitrate=1100;s.render.ffmpeg.maxrate=1300;s.render.ffmpeg.minrate=0;s.render.ffmpeg.buffersize=1792;s.render.ffmpeg.audio_codec='NONE';s.render.filepath=OUT+'/course_6_highlights.mp4'
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/course_6_highlights_edit.blend')
# Check representative frames from all five clips.
for i,item in enumerate(meta):
 s.frame_set(item['timeline_start']+round(item['duration_seconds']*fps/2));s.render.image_settings.file_format='PNG';s.render.filepath=OUT+f'/highlight_check_{i+1}.png';bpy.ops.render.render(write_still=True)
s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.constant_rate_factor='NONE';s.render.ffmpeg.video_bitrate=1100;s.render.ffmpeg.maxrate=1300;s.render.ffmpeg.buffersize=1792;s.render.filepath=OUT+'/course_6_highlights.mp4';bpy.ops.render.render(animation=True)
for p in glob.glob(OUT+'/course_6_highlights.mp4*.mp4'):os.replace(p,OUT+'/course_6_highlights.mp4')
size=os.path.getsize(OUT+'/course_6_highlights.mp4');assert size<=5000000,size
with open(OUT+'/highlights_6_edit.json','w') as f:json.dump({'duration_seconds':(frame-1)/fps,'bytes':size,'clips':meta},f,indent=2)
print('HIGHLIGHTS_6_COMPLETE',size,flush=True)
