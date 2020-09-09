#!/usr/bin/env bash

# Generates input sentences in jsonl format ready for Prodigy annotation
# Runs in parallel - this may create excessive load on the Scholarcy API server so use with care
# Usage: cos_score_parallel_sentences_prodigy.sh <path to pdf dir> <endpoint> <output dir> auth_token
if [ -n "$4" ]
then
   auth="--header \"Authorization: Bearer $4\""
else
   auth=''
fi

find "$1" -type f \( -iname \*.pdf -o -iname \*.pptx -o -iname \*.docx -o -iname \*.rtf -o -iname \*.htm \) -print | while read filename;
do
    f=$(basename "${filename%.*}")
    echo "curl -X POST $auth -F \"file=@$filename\" -F \"separate_sentences=true\" \"$2/api/metadata/basic\" | jq -c '{text: (.structured_content[].content[][]? + \".\")}' > \"$3/$f.jsonl\" " ;
done | parallel eval