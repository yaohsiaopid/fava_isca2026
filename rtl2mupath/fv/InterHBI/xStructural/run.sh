#!/bin/bash
if [ -f meta.txt ]; then 
mv meta.txt meta.old
fi 
python3 genall_pair.py gen
