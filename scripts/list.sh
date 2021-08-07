#!/bin/bash
if [ ! -d captures ]; then
  mkdir -p captures;
fi
if [ ! -d capture-summaries ]; then
  mkdir -p capture-summaries;
fi
python3 scripts/list.py $1