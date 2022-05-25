#!/bin/bash

version=$1

docker_repo="ghcr.io/masami10/onesphere_reporter/server"

docker build --no-cache --build-arg BUILD_ENV=LOCAL -t ${docker_repo}:"${version}" .
