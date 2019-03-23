#!/bin/bash
while true; do
    echo 1
    iwconfig $1 channel 1
    sleep 3s
    echo 6
    iwconfig $1 channel 6
    sleep 3s
    echo 11
    iwconfig $1 channel 11
    sleep 3s
done
