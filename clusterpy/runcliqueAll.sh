#!/bin/bash

DataDir=$1
find $DataDir -name "*.ids" -print -exec ./runclique.sh {} \;
