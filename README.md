# Installation

- Install Python 3 if not already installed
- Create a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

- Install the dependencies:

```
pip install -r requirements.txt
```

- Run the tests

```
nosetests -v
```

# Usage

The main purpose of this script is to:
- identify candidate sentences that appear to contain data availability or study registration sentences.
- generate a patterns file for use in Prodigy to create candidate annotations for these statements.

```
python main.py /path/to/file.txt
```


# Prodigy recipe

First create some input data that can be used within Prodigy for active learning and annotation.
The `cos_score_serial_sentences_prodigy.sh` script can be used for this - it processes pdf, docx, xml 
and other file formats into the sentence-level jsonl format required by Prodigy.

This script will omit the References section from each input PDF. 
Still, you may wish to filter out noisy lines, such as titles, authors, affiliations etc.
You could filter out lines less than a certain length, for example.

Next, we need to teach Prodigy to label the data, using the `registration_patterns.jsonl` file as a guide.
You will do this by running an annotation session, one file at a time.
See `ner.teach` in https://prodi.gy/docs/recipes#ner

```
prodigy ner.teach ner_score_registrations en_core_web_sm /path/to/file/eg/Imhoff_JournExpSocPsych_2018_jJ.jsonl  --label TRIAL_REGISTRATION_ID,DATA_AVAILABILITY --patterns ./registration_patterns.jsonl
```

As the input `.jsonl` files should already be sentence-delimited, 
you might want to try adding the `--unsegmented` parameter to the above command

Launch your browser at http://localhost:8080 and start correcting the annotations generated.

Accept or reject the annotations created, and when you have finished, 
make sure to click the Save button in the top left hand corner to save the output.