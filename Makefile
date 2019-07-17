BASE_IMAGE=slikshooz/gif-maker:latest
IMAGE=slikshooz/gif-a-meme:latest

build:
	go build -o meme
build-linux:
	GOOS=linux CGO_ENABLED=0 go build -o meme-publish

docker-build-base:
	docker build -t  $(BASE_IMAGE) -f Dockerfile.base .

docker-build: docker-build-base
	docker build -t $(IMAGE) -f Dockerfile .

run:
	docker run --rm -ti -v /tmp/darren:/usr/src/share $(IMAGE)
