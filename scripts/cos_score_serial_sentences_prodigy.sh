#!/usr/bin/env bash

# Generates input sentences in jsonl format ready for Prodigy annotation
# Runs sequentially to prevent excessive load on Scholarcy API server
# Usage: cos_score_serial_sentences_prodigy.sh <path to pdf dir> <endpoint> <output dir> auth_token
if [[ -n "$4" ]]
then
   auth="Authorization: Bearer $4"
else
   auth=''
fi

find "$1" -type f \( -iname \*.pdf -o -iname \*.pptx -o -iname \*.docx -o -iname \*.rtf -o -iname \*.htm \) -print | while read filename;
do
    f=$(basename "${filename%.*}")
    curl -X POST --header "${auth}" -F "file=@$filename" -F "separate_sentences=true" "$2/api/metadata/basic" | jq -c '{text: (.structured_content[].content[][]? + ".")}' > "$3/$f.jsonl" ;
done