#!/bin/sh

if [ -f /usr/src/share/subtitles.yaml ]; then
    cp /usr/src/share/subtitles.yaml /usr/src/app/subtitles.yaml
fi

meme

if [ -f  /usr/src/app/result.gif ]; then
    cp  /usr/src/app/result.gif /usr/src/share/result.gif
fi 
