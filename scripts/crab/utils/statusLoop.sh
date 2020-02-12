#!/bin/bash

source setup.sh

while true
do
    crab status $1
    sleep 300
done