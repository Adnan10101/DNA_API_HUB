#!/bin/bash

echo "Building docker image......"
echo "Enter Version...."
read DOCKER_IMAGE_TAG
DOCKER_IMAGE_NAME="dna-api-hub"
DOCKER_REGISTRY="adnan10101"
RELEASE_NAME="dna-api-hub"
# CHART_REPO="/home/dna1pe3/projects/auto_mount/deploy"
# DOCKERFILE_REPO="/home/dna1pe3/projects/auto_mount"

sudo docker build -t $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG .

echo "Pushing docker image to dockerhub...."
sudo docker tag $DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG $DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG
sudo docker push $DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_TAG

echo "Checking if AutoMount helm Release already exists....."
if helm list | grep $RELEASE_NAME; then
    echo "AutoMount Release already exists, upgrading....."
    helm upgrade $RELEASE_NAME deploy/ -f deploy/values.yaml --set deployment.tag=$DOCKER_IMAGE_TAG
    if [ $? -ne 0 ]; then
        echo "Failed to delete Helm Relase. Exiting."
        exit 1
    fi
else
    echo "AutoMount deployment does not exist. Installing....."
    helm install $RELEASE_NAME deploy/
    if [ $? -ne 0 ]; then
        echo "Failed to install Helm release. Exiting."
        exit 1
    fi
fi
