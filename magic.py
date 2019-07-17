#!/usr/bin/env python3

import click
import os
import sys
import tempfile

from operations.gif_it import GenerateGifIt

@click.command()
@click.option('--output', '-o', default='/usr/src/share/results.gif', type=str)
def main(output):
    temp_dir = tempfile.mkdtemp()

    config = {
        'avi_path': os.path.join(temp_dir, 'nosub.avi'),
        'final_path': os.path.join(temp_dir, 'final.avi'),
        'output_path': '/usr/src/share/meme.gif',
        'source_path': os.path.join(temp_dir, 'sourceVideo.mp4'),
        'subtitle_path': '/usr/src/share/subtitles.yaml',
        'temp_dir': temp_dir,
        'video_quality': 135,
        'video_url': 'https://www.youtube.com/watch?v=CGOPPzh8TJ4'
    }
    
    generator = GenerateGifIt()
    cmd = generator.get_instance()
    
    result = cmd.exec(config)
    if result is None:
        sys.exit(1)
    
    sys.exit(0)
    

if __name__ == '__main__':
    main()
