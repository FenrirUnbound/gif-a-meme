IMAGE=slikshooz/gif-a-meme:latest

build:
	go build -o meme
build-linux:
	GOOS=linux CGO_ENABLED=0 go build -o meme-publish

docker-build:
	GOOS=linux CGO_ENABLED=0 go build -o meme-publish
	cp meme-publish ./exports/meme
	cp subs_only.py ./exports/subs_only.py
	docker build -t $(IMAGE) -f Dockerfile .
