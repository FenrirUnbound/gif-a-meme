#!/usr/bin/env python3

import click
import os
import sys
import tempfile

from operations.gif_it import GenerateGifIt

DEFAULT_VIDEO = 'https://www.youtube.com/watch?v=CGOPPzh8TJ4'
SHARE_DIR = '/usr/src/share'
VIDEO_QUALITY = 'context_video_quality'

def _generate_config(overrides={}):
    temp_dir = tempfile.mkdtemp()

    avi_path = os.path.join(temp_dir, 'nosub.avi')
    if 'input_video' in overrides:
        avi_path = os.path.join(SHARE_DIR, overrides['input_video'])

    source_path = os.path.join(temp_dir, 'sourceVideo.mp4')
    if 'video_save_path' in overrides:
        source_path = overrides['video_save_path']

    return {
        'avi_path': avi_path,
        'final_path': os.path.join(temp_dir, 'final.avi'),
        'output_path': os.path.join(SHARE_DIR, overrides['output_path']),
        'source_path': source_path,
        'subtitle_path': '/usr/src/share/subtitles.yaml',
        'temp_dir': temp_dir,
        'video_quality': overrides['video_quality'],
        'video_url': overrides['video_url'] if 'video_url' in overrides else DEFAULT_VIDEO
    }

@click.group()
@click.option('--video-quality', '-q', default=135, type=int)
@click.pass_context
def cli(ctx, video_quality):
    ctx.ensure_object(dict)

    ctx.obj[VIDEO_QUALITY] = video_quality

@cli.command()
@click.option('--output', '-o', default='/usr/src/share/results.gif', type=str)
@click.option('--input-video', '-i', default='', type=str)
@click.pass_context
def run(ctx, output, input_video):
    """Runs the entire recipe: download, conversion, subtitle, save"""
    overrides = {
        'input_video': input_video,
        'output_path': output,
        'video_quality': ctx.obj[VIDEO_QUALITY]
    }
    config = _generate_config(overrides=overrides)
    
    generator = GenerateGifIt()
    cmd = generator.get_instance({
        'skip_download': len(input_video) > 0
    })
    
    exit_code = cmd.exec(config)
    sys.exit(exit_code)

@cli.command()
@click.option('--info', is_flag=True)
@click.argument('url')
@click.pass_context
def download(ctx, info, url):
    """Download the desired video"""
    config = _generate_config({
        'output_path': '/usr/src/share/results.gif',  # todo: remove this
        'video_quality': ctx.obj[VIDEO_QUALITY],
        'video_save_path': os.path.join(SHARE_DIR, 'video.mp4'),
        'video_url': url
    })
    cmd = None

    generator = GenerateGifIt()
    if info:
        cmd = generator.get_video_options()
    else:
        cmd = generator.get_downloader()

    exit_code = cmd.exec(config=config)
    sys.exit(exit_code)

if __name__ == '__main__':
    cli(obj={})
