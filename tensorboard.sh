#! /bin/bash

. ./env/bin/activate
tensorboard --logdir=./experiments --port=133
