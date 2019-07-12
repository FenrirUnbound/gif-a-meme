#!/usr/bin/env python3

import json
import sys
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import os
import shutil

def decode_subdata(input):
    result =[]
    
    # 720x480
    font_size = 60
    bottom_align = 480-font_size
    left_align = 720/2
    
    subtitle_data = json.loads(input)
    print(subtitle_data)
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

def makePngSub(text, color, position, filename, temp_dir):
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


def subVideo(subs,inputvid,outputvid,temp_dir):
    """Take a list a subtitles, make each png with makePngSub()
    and add the pngs to the video at the given intervals"""
    n=1
    subfiles=[]
    for sub in subs:
        subfile = makePngSub(text=sub[0],color=sub[1],
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

def main(temp_dir, input_video, output_video, subtitle_data):
    # todo: refactor this to input
    white=(255,255,255)
    yellow=(255,233,155)
    subs = decode_subdata(subtitle_data)
    subVideo(subs=subs,inputvid=input_video,outputvid=output_video,temp_dir=temp_dir)
    

if __name__ == '__main__':
    if len(sys.argv) != 4+1:
        print('Need 4 inputs')
        print('{}'.format(str(sys.argv)))
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])