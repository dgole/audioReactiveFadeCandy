#!/bin/bash

cd /home/lights/projects/audioReactiveFadeCandy/bm2019
gnome-terminal &
echo lights | sudo -S /usr/local/bin/fcserver /home/lights/projects/audioReactiveFadeCandy/bm2019/fcserver.json

