#!/bin/sh

docker build -t app-test --target test .

docker run --rm \
    --volume=`pwd`/src:/usr/src/app \
    app-test