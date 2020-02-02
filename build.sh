#!/bin/bash -exv

fullname=tweet-cleanup
docker build --tag="$fullname:latest" \
  --tag="docker-registry.home.tedder.me/$fullname:latest" \
  --force-rm=true --compress=true .
docker push "docker-registry.home.tedder.me/$fullname:latest"

if [[ $? != 0 ]]
then
  echo "Build of $fullname FAILED"
  exit -1
fi

