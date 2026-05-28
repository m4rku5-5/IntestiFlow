#!/bin/bash

coords="$(python3 get_coords.py $1 $2)"

echo ${coords}

python3 gutImager_v2.py $1 ${coords} $2
