BASE_IMAGE=slikshooz/gif-maker:latest
IMAGE=slikshooz/gif-a-meme:latest

build:
	go build -o meme
build-linux:
	GOOS=linux CGO_ENABLED=0 go build -o meme-publish

.PHONY: docker-build-base
docker-build-base:
	docker build -t  $(BASE_IMAGE) -f Dockerfile.base .

.PHONY: docker-build
docker-build: docker-build-base
	docker build -t $(IMAGE) -f Dockerfile .

.PHONY: docker-push
docker-push:
	docker login -u $(DOCKER_USER) -p $(DOCKER_PASS) docker.io
	docker push $(IMAGE)

run:
	docker run --rm -ti -v /tmp/darren:/usr/src/share $(IMAGE)
