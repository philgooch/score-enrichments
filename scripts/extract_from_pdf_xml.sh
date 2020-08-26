#!/usr/bin/env bash

# Usage: extract_from_pdf_xml.sh <path to pdf-xml dir> <output dir>

find "$1" -iname *.xml -print | while read filename;
do
    f=$(basename "${filename%.*}")
    python main.py "${filename}" > "$2/$f.txt";
done