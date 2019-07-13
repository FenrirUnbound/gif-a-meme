# GIF A Meme

## Table of Contents
+ [About](#about)
+ [Getting Started](#getting_started)
+ [Usage](#usage)
+ [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

Simplify the process of adding gif-like dialogue to a GIF.

## Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

* Docker

### Installing

You can choose to pull the Docker image that's already published to Docker Hub

```
$ docker pull slikshooz/gif-a-meme:latest
```

If you prefer to build your own Docker image based on the current state of the repository, you can run the following Make commands:

```
# In order to name the image differently
$ export IMAGE=myUsername/my-gif-a-meme:latest

# creates the docker image
$ make docker-build

# Executes your local image
$ make run
```

## Usage <a name = "usage"></a>

Edit the `subtitles.yaml` file with your script, then run the docker image

```
# /tmp/myStuff is the folder that contains the subtitles.yaml & where the 
# resulting gif will be stored
$ docker run --rm -ti \  
  -v /tmp/myStuff:/usr/src/share \
  slikshooz/gif-a-meme:latest
```
