#!/bin/bash

my_FILES=$(grep -E ".*_S$1_.*" sorted_list_of_files.txt)

kallisto quant -i *.idx -o "output/S$1"  $my_FILES 


