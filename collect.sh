#!/bin/bash --debug
pkill python
rm collect.log
touch collect.log
nohup bash -c '. /home/apara/python-env/solar2/bin/activate;python main.py' > collect.log 2>&1 &
tail -f collect.log
