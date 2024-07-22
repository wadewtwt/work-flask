#!/bin/bash
git pull
docker build -t python38-image .
docker run -dit -p 13003:13003 -v /www/work-flask:/www --name python38-container --restart=always python38-image