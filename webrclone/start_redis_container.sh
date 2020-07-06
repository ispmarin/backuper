#!/bin/bash

docker run --publish 6379:6379 --detach --name redis-container redis
