#!/usr/bin/env bash
set -o xtrace
set -e

#deploy an image 
export DOCKER_REGISTRY=us.gcr.io/adria-health
export DOCKER_IMG_NAME=skyspace-api
export GIT_IMG_TAG=`git rev-parse --verify HEAD`

# Build the docker image
docker build -t $DOCKER_IMG_NAME .

# Tag the image
docker tag $DOCKER_IMG_NAME $DOCKER_REGISTRY/$DOCKER_IMG_NAME
docker tag $DOCKER_IMG_NAME $DOCKER_REGISTRY/$DOCKER_IMG_NAME:$GIT_IMG_TAG

docker push "${DOCKER_REGISTRY}/${DOCKER_IMG_NAME}:$GIT_IMG_TAG"
docker push "${DOCKER_REGISTRY}/${DOCKER_IMG_NAME}:latest" 

# To update an existing deployment with a new image.
kubectl set image deployment/skyspace-api skyspace-api=$DOCKER_REGISTRY/$DOCKER_IMG_NAME:$GIT_IMG_TAG