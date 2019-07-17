#!/usr/bin/env python3

import click
import os
import sys
import tempfile

from operations.gif_it import GenerateGifIt

SHARE_DIR = '/usr/src/share'

@click.command()
@click.option('--output', '-o', default='/usr/src/share/results.gif', type=str)
@click.option('--input-video', '-i', default='', type=str)
def main(output, input_video):
    temp_dir = tempfile.mkdtemp()
    skip_download = len(input_video) > 0

    avi_path = os.path.join(temp_dir, 'nosub.avi')
    if skip_download:
        avi_path = os.path.join(SHARE_DIR, input_video)

    config = {
        'avi_path': avi_path,
        'final_path': os.path.join(temp_dir, 'final.avi'),
        'output_path': os.path.join(SHARE_DIR, output),
        'source_path': os.path.join(temp_dir, 'sourceVideo.mp4'),
        'subtitle_path': '/usr/src/share/subtitles.yaml',
        'temp_dir': temp_dir,
        'video_quality': 135,
        'video_url': 'https://www.youtube.com/watch?v=CGOPPzh8TJ4'
    }
    
    generator = GenerateGifIt()
    cmd = generator.get_instance({
        'skip_download': skip_download
    })
    
    result = cmd.exec(config)
    if result is None:
        sys.exit(1)
    
    sys.exit(0)
    

if __name__ == '__main__':
    main()
