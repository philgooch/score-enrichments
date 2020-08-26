#!/usr/bin/env bash

# Usage: extract_from_pdf_xml.sh <path to pdf-xml dir> <output dir>

find "$1" -iname *.xml -print | while read filename;
do
    f=$(basename "${filename%.*}")
    cat "${filename}" | grep '<pre ' | while read -r line ;
    do
        python main.py "${line}" >> "$2/$f.txt";
    done
done