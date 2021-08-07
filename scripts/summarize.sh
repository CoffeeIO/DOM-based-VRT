#!/bin/bash
if [ ! -d comparisons ]; then
  mkdir -p comparisons;
fi
python3 scripts/summarize.py $1