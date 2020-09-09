#!/usr/bin/env bash

# Parallelised version of extract_from_pdf_xml.sh - much faster but may cause your computer to overheat!
# Usage: extract_from_pdf_xml_parallel.sh <path to pdf-xml dir> <output dir>

find "$1" -iname *.xml -print | while read filename;
do
    f=$(basename "${filename%.*}")
    echo "python main.py \"${filename}\" > \"$2/$f.txt\" ";
done | parallel eval