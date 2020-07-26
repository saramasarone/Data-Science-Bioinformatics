#!/bin/bash
awk 'BEGIN {FS="/"; OFS="|"}{print $NF,$0}' list_of_files.txt | sort -t"/" -k4,4 | sort -t"_" -k2,2 -V -s | awk -F "|" '{print $NF}' > sorted_list_of_files.txt

