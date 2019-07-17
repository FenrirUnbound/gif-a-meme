import json
import os
import sys
import yaml
import PIL

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from operations.chain import Chain

class Subtitle(Chain):
    def __init__(self, nextOp=None):
        super(Subtitle, self).__init__(nextOp=nextOp)

    def _exec(self, config={}):
        subtitle_data = {}

        with open(config['subtitle_path'], 'r') as f:
            try:
                subtitle_data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                print('[error] Received error from executing: {}'.format(e), file=sys.stderr)
                return 1
        
        # todo: refactor this
        white = (255,255,255)
        yellow = (255,233,155)
        subs = self._decode_subdata(subtitle_data)
        
        self._subVideo(
            subs=subs,
            inputvid=config['avi_path'],
            outputvid=config['final_path'],
            temp_dir=config['temp_dir']
            )
        return 0

    def _decode_subdata(self, subtitle_data):
        result =[]
        
        # 720x480
        font_size = 60
        bottom_align = 480-font_size
        left_align = 720/2
        
        for sub in subtitle_data['subtitles']:
            entry = [
                sub['message'],
                sub['color'],
                # position is static
                (left_align,bottom_align),
                '{},{}'.format(sub['start_time'], sub['end_time'])
            ]
            
            result.append(entry)
        print(result)

        return result

    def _makePngSub(self, text, color, position, filename, temp_dir):
        """"Turn a text into a png"""
        # todo: make these configurable
        font_size=60
        # 720x480
        video_width=720
        video_height=480

        # img = Image.new('RGBA',(1280, 544))
        img = Image.new('RGBA',(video_width, video_height))
        x,y = position
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("Ubuntu-B.ttf",font_size)
        w, h = draw.multiline_textsize(text, font=font)
        x = x - w/2
        y = y - h/2
        for i in range(1,6):
            draw.multiline_text((x+i,y+i), text, fill=(0,0,0), font=font, align='center')
        draw.multiline_text((x,y), text, fill=color, font=font, align='center')
        filename = '{}/{}.png'.format(temp_dir,filename)
        img.save(filename, 'PNG')
        return filename
    
    def _subVideo(self, subs,inputvid,outputvid,temp_dir):
        """Take a list a subtitles, make each png with makePngSub()
        and add the pngs to the video at the given intervals"""
        n=1
        subfiles=[]
        for sub in subs:
            subfile = self._makePngSub(text=sub[0],color=sub[1],
                                position=sub[2],filename=str(n),temp_dir=temp_dir)
            subfiles.append(subfile)
            n+=1

        def writeFilterblocks(subs):
            """write the complex filter to chain-add all the png in one shot"""
            n = 0
            filter_blocks=[]
            for sub in subs:
                timing = sub[3]
                blocks=['']*4
                if n==0:
                    blocks[0]='"[0:v]'
                else:
                    blocks[0]='[tmp]'
                n+=1
                blocks[1]='['+str(n)+':v]'
                blocks[2]="overlay=enable='between(t,{})'".format(timing)
                if n!=len(subs):
                    blocks[3]=' [tmp]; '
                else:
                    blocks[3]='"'
                filter_blocks+=blocks
            return filter_blocks

        inputblocks = ['ffmpeg -i '+inputvid]+['-i '+subfile for subfile in subfiles]
        inputstr = ' '.join(inputblocks)
        filterstr = '-filter_complex '+''.join(writeFilterblocks(subs))
        #outputstr = '-y '+ outputvid
        outputstr = '-y -c:v ffv1 '+ outputvid
        command = inputstr+' '+filterstr+' '+outputstr
        os.system(command)