FROM slikshooz/gif-maker:latest
MAINTAINER Darren Matsumoto <darren@matsumoto.io>

COPY . /usr/src/app

ENTRYPOINT ["python3", "/usr/src/app/magic.py"]
CMD ["run"]
