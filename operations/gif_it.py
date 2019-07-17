import json
import os
import sys

from abc import abstractmethod
from operations.chain import Chain
from operations.command import Command
from operations.subtitles import Subtitle

class GenerateGifIt(object):
    def get_instance(self, options={}):
        instance = self.__create_instance(options)
        
        return instance
    
    def __create_instance(self, options={}):
        first = None

        if not options['skip_download']:
            first = DownloadVideo(nextOp=ConvertAVI())
        else:
            first = ConvertAVI()
        
        first.add_chain(to_add=Subtitle())
        first.add_chain(to_add=PublishGif())

        return first

    def get_downloader(self, options={}):
        return DownloadVideo()

class DownloadVideo(Chain):
    def __init__(self, nextOp=None):
        super(DownloadVideo, self).__init__(nextOp=nextOp)
    
    def _exec(self, config={}):
        cmd = 'youtube-dl'
        args = [
            '-f', config['video_quality'],
            '-o', config['source_path'],
            config['video_url']
        ]

        return self.command.run(cmd=cmd, args=args)

class ConvertAVI(Chain):
    def __init__(self, nextOp=None):
        super(ConvertAVI, self).__init__(nextOp=nextOp)
    
    def _exec(self, config={}):
        cmd = 'ffmpeg'
        args = [
            '-i', config['source_path'],
            '-c', 'copy',
            '-y',
            config['avi_path']
        ]

        return self.command.run(cmd=cmd, args=args)

class PublishGif(Chain):
    def __init__(self, nextOp=None):
        super(PublishGif, self).__init__(nextOp=nextOp)

    def _exec(self, config={}):
        palette_path = os.path.join(config['temp_dir'], 'palette.png')
        
        cmd = 'ffmpeg'
        args = [
            '-i', config['final_path'],
            '-vf', 'fps=24,scale=1080:-1:flags=lanczos,palettegen',
            '-y',
            palette_path
        ]

        exit_code = self.command.run(cmd=cmd, args=args)
        if exit_code > 0:
            return exit_code

        args = [
            '-i', config['final_path'],
            '-i', palette_path,
            '-filter_complex', '"fps=24,scale=1080:-1:flags=lanczos[x];[x][1:v]paletteuse"',
            config['output_path']
        ]

        return self.command.run(cmd=cmd, args=args)
