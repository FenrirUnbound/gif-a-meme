FROM slikshooz/gif-maker:latest
MAINTAINER Darren Matsumoto <darren@matsumoto.io>

COPY ./exports /usr/src/app
RUN cp /usr/src/app/subs_only.py /usr/local/bin/subs_only.py \
  && cp /usr/src/app/meme /usr/local/bin/meme

ENTRYPOINT ["./entrypoint.sh"]
