import sys
import os
import logging
from spacy.lang.en import English
from spacy.pipeline import EntityRuler

log = logging.getLogger(__name__)

TRIAL_LABEL = "TRIAL_REGISTRATION_ID"

# TODO: We can probably combine some of these patterns, e.g. NCT|DRKS|ISRCTN
# ClinicalTrials.gov
NCT_PATTERN_1 = [{'TEXT': {"REGEX": "^NCT[-\u2010-\u2013/]?[0-9]{8}(?=[.,:;)]|$)"}}]
NCT_PATTERN_2 = [{'ORTH': "NCT"},
                 {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                 {'TEXT': {"REGEX": "^[0-9]{8}(?=[.,:;)]|$)"}}]

# ANZCTR:
ANZ_PATTERN_1 = [{'TEXT': {"REGEX": "^ACTRN[-\u2010-\u2013/]?[0-9]{14}(?=[.,:;)]|$)"}}]
ANZ_PATTERN_2 = [{'ORTH': "ACTRN", "OP": "?"}, {'TEXT': {"REGEX": "^126[0-9]{11}(?=[.,:;)]|$)"}}]

# Universal trial number
# U1111-1254-7316
UTN_PATTERN = [{'TEXT': {"REGEX": "^U[0-9]{4}[-\u2010-\u2013/]?[0-9]{4}[-\u2010-\u2013/]?[0-9]{4}(?=[.,:;)]|$)"}}]

# DRKS
# DRKS00000002
DRKS_PATTERN_1 = [{'TEXT': {"REGEX": "^DRKS[-\u2010-\u2013/]?[0-9]{8}(?=[.,:;)]|$)"}}]
DRKS_PATTERN_2 = [{'ORTH': "DRKS"},
                  {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                  {'TEXT': {"REGEX": "^[0-9]{8}(?=[.,:;)]|$)"}}]

# ISRCTN
# ISRCTN14702259
ISRCTN_PATTERN_1 = [{'TEXT': {"REGEX": "^ISRCTN[-\u2010-\u2013/]?[0-9]{8}(?=[.,:;)]|$)"}}]
ISRCTN_PATTERN_2 = [{'ORTH': "ISRCTN"},
                  {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                  {'TEXT': {"REGEX": "^[0-9]{8}(?=[.,:;)]|$)"}}]


# CRD
# CRD42020179519
# https://www.crd.york.ac.uk/prospero/display_record.php?RecordID=179519
CRD_PATTERN_1 = [{'TEXT': {"REGEX": "^CRD[-\u2010-\u2013/]?[0-9]{11}(?=[.,:;)]|$)"}}]
CRD_PATTERN_2 = [{'ORTH': "CRD"},
                  {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                  {'TEXT': {"REGEX": "^[0-9]{11}(?=[.,:;)]|$)"}}]


# JPRN
# https://apps.who.int/trialsearch/Trial2.aspx?TrialID=JPRN-UMIN000040928
JPRN_PATTERN_1 = [{'TEXT': {"REGEX": "^JPRN[-\u2010-\u2013/]?UMIN[-\u2010-\u2013/]?[0-9]{9}(?=[.,:;)]|$)"}}]
JPRN_PATTERN_2 = [{'ORTH': "JPRN"},
                  {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                  {'TEXT': {"REGEX": "^UMIN[-\u2010-\u2013/]?[0-9]{9}(?=[.,:;)]|$)"}}]
JPRN_PATTERN_3 = [{'ORTH': "JPRN"},
                  {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                  {'ORTH': "UMIN"},
                  {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                  {'TEXT': {"REGEX": "^[0-9]{9}(?=[.,:;)]|$)"}}]

# ChiCTR
# http://www.chictr.org.cn/showprojen.aspx?proj=57931
CHICTR_PATTERN_1 = [{'TEXT': {"REGEX": "^ChiCTR[-\u2010-\u2013/]?(IIR[-\u2010-\u2013/]?)?[0-9]{8,10}(?=[.,:;)]|$)"}}]
CHICTR_PATTERN_2 = [{'ORTH': "ChiCTR"},
                  {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                  {'TEXT': {"REGEX": "^IIR[-\u2010-\u2013/]?[0-9]{8,10}(?=[.,:;)]|$)"}}]
CHICTR_PATTERN_3 = [{'ORTH': "ChiCTR"},
                  {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                  {'ORTH': "IIR", "OP": "?"},
                  {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                  {'TEXT': {"REGEX": "^[0-9]{8,10}(?=[.,:;)]|$)"}}]


# PACTR
# PACTR202008685699453
# https://apps.who.int/trialsearch/Trial2.aspx?TrialID=PACTR202008685699453
PACTR_PATTERN_1 = [{'TEXT': {"REGEX": "^PACTR[-\u2010-\u2013/]?[0-9]{15}(?=[.,:;)]|$)"}}]
PACTR_PATTERN_2 = [{'ORTH': "PACTR"},
                  {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                  {'TEXT': {"REGEX": "^[0-9]{15}(?=[.,:;)]|$)"}}]


# KCT
# KCT0005285
# https://apps.who.int/trialsearch/Trial2.aspx?TrialID=KCT0005285
KCT_PATTERN_1 = [{'TEXT': {"REGEX": "^KCT[-\u2010-\u2013/]?[0-9]{7}(?=[.,:;)]|$)$"}}]
KCT_PATTERN_2 = [{'ORTH': "KCT"},
                  {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                  {'TEXT': {"REGEX": "^[0-9]{7}(?=[.,:;)]|$)$"}}]

# https://aspredicted.org/
ASP_PATTERN = [{'TEXT': {"REGEX": "^https?://aspredicted.org/.+$"}}]


def file_to_text(file_path):
    doc_text = ''
    with open(file_path, 'rb') as f:
        try:
            doc_text = f.read().decode('utf-8-sig')
        except UnicodeDecodeError:
            try:
                doc_text = f.read().decode('utf-8')
            except UnicodeDecodeError:
                try:
                    doc_text = f.read().decode('latin-1')
                except UnicodeDecodeError as e:
                    log.error("{}: Text encoding problem with {}".format(e, file_path))
    return doc_text


def main(file_path_or_input_text=None):
    nlp = English()
    ruler = EntityRuler(nlp)
    patterns = [
        {"label": TRIAL_LABEL, "pattern": NCT_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": NCT_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": ANZ_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": ANZ_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": UTN_PATTERN},
        {"label": TRIAL_LABEL, "pattern": DRKS_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": DRKS_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": ISRCTN_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": ISRCTN_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": CRD_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": CRD_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": JPRN_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": JPRN_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": JPRN_PATTERN_3},
        {"label": TRIAL_LABEL, "pattern": CHICTR_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": CHICTR_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": CHICTR_PATTERN_3},
        {"label": TRIAL_LABEL, "pattern": PACTR_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": PACTR_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": KCT_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": KCT_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": ASP_PATTERN},
    ]
    ruler.add_patterns(patterns)
    nlp.add_pipe(ruler)
    nlp.add_pipe(nlp.create_pipe('sentencizer'))

    if os.path.isfile(file_path_or_input_text):
        doc_text = file_to_text(file_path_or_input_text)
    else:
        doc_text = file_path_or_input_text
    doc = nlp(doc_text)
    # Output patterns to disk
    ruler.to_disk("./registration_patterns.jsonl")
    for sent in doc.sents:
        for ent in sent.ents:
            if ent:
                print(sent, ent.text, ent.label_)


if __name__ == "__main__":
    args = sys.argv
    main(args[1])
