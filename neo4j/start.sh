#!/bin/bash

set -m

/docker-entrypoint.sh neo4j &

./dbConfig.sh 

fg %1
