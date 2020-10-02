import sys
import os
import re
import logging
from spacy.lang.en import English
from spacy.pipeline import EntityRuler

log = logging.getLogger(__name__)

TRIAL_LABEL = "TRIAL_REGISTRATION_ID"
DATA_AVAILABILITY_LABEL_URL = "DATA_AVAILABILITY_OPEN_URL"
DATA_AVAILABILITY_LABEL_SUPPL = "DATA_AVAILABILITY_OPEN_SUPPLEMENT"
DATA_AVAILABILITY_LABEL_CLOSED = "DATA_AVAILABILITY_CLOSED"

DATA_AVAILABILITY_PATTERN_URL = [{'TEXT': {
    "REGEX": "^([Ss]upplementary|[Ss]upporting|[Ss]ource|[Cc]omputer|[Pp]rogram|[Ee]xperiment(al)?|[Aa]nonymi[sz]ed)$"},
    "OP": "?"},
    {"ORTH": ",", "OP": "?"}, {"IS_ALPHA": True, "OP": "?"}, {"ORTH": "-", "OP": "?"},
    {"ORTH": ",", "OP": "?"}, {"IS_ALPHA": True, "OP": "?"}, {"ORTH": "-", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {'TEXT': {
        "REGEX": "^([Cc]odes?|[Ff]iles|[Dd]ata(sets)?|[Mm]odels?|[Ss]scripts?|[Ss]oftware|[Ii]nformation)$"}},
    {"ORTH": "sets", "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {'TEXT': {"REGEX": "^(and|&)$"}, "OP": "?"},
    {'TEXT': {
        "REGEX": "^([Cc]odes?|[Ff]iles|[Dd]ata(sets)?|[Mm]odels?|[Ss]scripts?|[Ss]oftware|[Ii]nformation)$"},
        "OP": "?"},
    {"ORTH": "sets", "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {'TEXT': {"REGEX": "^(and|&)$"}, "OP": "?"},
    {'TEXT': {
        "REGEX": "^([Cc]odes?|[Ff]iles|[Dd]ata(sets)?|[Mm]odels?|[Ss]scripts?|[Ss]oftware|[Ii]nformation)$"},
        "OP": "?"},
    {"ORTH": "sets", "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {'TEXT': {"REGEX": "^(and|&)$"}, "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {'TEXT': {"REGEX": "^(is|are|can|may|will|has|have)$"}},
    {'TEXT': {"REGEX": "^(be|been)$"}, "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {'TEXT': {"REGEX": "^(available|found|deposited|provided)$"}},
    {"ORTH": ",", "OP": "?"},
    {"ORTH": "(", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"ORTH": ")", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"ORTH": ")", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"ORTH": ")", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"ORTH": ")", "OP": "?"},
    {'TEXT': {"REGEX": "^(at|on|from|in|to|without)$"}},
    {"ORTH": "restriction", "OP": "?"},
    {"ORTH": ":", "OP": "?"},
    {"IS_ALPHA": True, "OP": "*"},
    {'TEXT': {"REGEX": "^[\u2019']s$"}, "OP": "?"},
    {"IS_ALPHA": True, "OP": "*"},
    {'TEXT': {"REGEX": "^[-0-9\u2010-\u2013]$"}, "OP": "*"},
    {"IS_ALPHA": True, "OP": "*"},
    {"ORTH": "(", "OP": "?"},
    {'TEXT': {"REGEX": "^(https?://.+|goo.gl/.+)$"}},
    {"ORTH": ")", "OP": "?"},
]

DATA_AVAILABILITY_PATTERN_CLOSED = [{'TEXT': {
    "REGEX": "^([Ss]upplementary|[Ss]upporting|[Ss]ource|[Cc]omputer|[Pp]rogram|[Ee]xperiment(al)?|[Aa]nonymi[sz]ed)$"},
    "OP": "?"},
    {"ORTH": ",", "OP": "?"}, {"IS_ALPHA": True, "OP": "?"}, {"ORTH": "-", "OP": "?"},
    {"ORTH": ",", "OP": "?"}, {"IS_ALPHA": True, "OP": "?"}, {"ORTH": "-", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {'TEXT': {
        "REGEX": "^([Cc]odes?|[Ff]iles|[Dd]ata(sets)?|[Mm]odels?|[Ss]scripts?|[Ss]oftware|[Ii]nformation)$"}},
    {"ORTH": "sets", "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {'TEXT': {"REGEX": "^(and|&)$"}, "OP": "?"},
    {'TEXT': {
        "REGEX": "^([Cc]odes?|[Ff]iles|[Dd]ata(sets)?|[Mm]odels?|[Ss]scripts?|[Ss]oftware|[Ii]nformation)$"},
        "OP": "?"},
    {"ORTH": "sets", "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {'TEXT': {"REGEX": "^(and|&)$"}, "OP": "?"},
    {'TEXT': {
        "REGEX": "^([Cc]odes?|[Ff]iles|[Dd]ata(sets)?|[Mm]odels?|[Ss]scripts?|[Ss]oftware|[Ii]nformation)$"},
        "OP": "?"},
    {"ORTH": "sets", "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {'TEXT': {"REGEX": "^(and|&)$"}, "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {'TEXT': {"REGEX": "^(is|are|can|may|will|has|have)$"}},
    {'TEXT': {"REGEX": "^(be|been)$"}, "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {'TEXT': {"REGEX": "^(available|requested|provided)$"}},
    {"ORTH": ",", "OP": "?"},
    {"ORTH": "(", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"ORTH": ")", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"ORTH": ")", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"ORTH": ")", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"ORTH": ")", "OP": "?"},
    {'TEXT': {"REGEX": "^(by|on|from)$"}},
    {"IS_ALPHA": True, "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {'TEXT': {"REGEX": "^(request|authors?)$"}}
]

DATA_AVAILABILITY_PATTERN_SUPPLEMENT = [{'TEXT': {
    "REGEX": "^([Ss]upplementary|[Ss]upporting|[Ss]ource|[Cc]omputer|[Pp]rogram|[Ee]xperiment(al)?|[Aa]nonymi[sz]ed)$"},
    "OP": "?"},
    {"ORTH": ",", "OP": "?"}, {"IS_ALPHA": True, "OP": "?"}, {"ORTH": "-", "OP": "?"},
    {"ORTH": ",", "OP": "?"}, {"IS_ALPHA": True, "OP": "?"}, {"ORTH": "-", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {'TEXT': {
        "REGEX": "^([Cc]odes?|[Ff]iles|[Dd]ata(sets)?|[Mm]odels?|[Ss]scripts?|[Ss]oftware|[Ii]nformation)$"}},
    {"ORTH": "sets", "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {'TEXT': {"REGEX": "^(and|&)$"}, "OP": "?"},
    {'TEXT': {
        "REGEX": "^([Cc]odes?|[Ff]iles|[Dd]ata(sets)?|[Mm]odels?|[Ss]scripts?|[Ss]oftware|[Ii]nformation)$"},
        "OP": "?"},
    {"ORTH": "sets", "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {'TEXT': {"REGEX": "^(and|&)$"}, "OP": "?"},
    {'TEXT': {
        "REGEX": "^([Cc]odes?|[Ff]iles|[Dd]ata(sets)?|[Mm]odels?|[Ss]scripts?|[Ss]oftware|[Ii]nformation)$"},
        "OP": "?"},
    {"ORTH": "sets", "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {'TEXT': {"REGEX": "^(and|&)$"}, "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {'TEXT': {"REGEX": "^(is|are|can|may|will|has|have)$"}},
    {'TEXT': {"REGEX": "^(be|been)$"}, "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {'TEXT': {"REGEX": "^(available|found|deposited|provided)$"}},
    {"ORTH": ",", "OP": "?"},
    {"ORTH": "(", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"ORTH": ")", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"ORTH": ")", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"ORTH": ")", "OP": "?"},
    {"IS_ALPHA": True, "OP": "?"},
    {"ORTH": ",", "OP": "?"},
    {"ORTH": ")", "OP": "?"},
    {'TEXT': {"REGEX": "^(at|on|in)$"}},
    {"IS_ALPHA": True, "OP": "*"},
    {'TEXT': {"REGEX": "^[\u2019']s$"}, "OP": "?"},
    {'TEXT': {"REGEX": "^([Ww]eb(site)?|[Oo]nline|[Ss]upplements?|[Aa]ppendix|[Aa]ppendices|[Aa]ccession)$"}},
    {"IS_ALPHA": True, "OP": "?"},
    {'TEXT': {"REGEX": "^[-0-9\u2010-\u2013]$"}, "OP": "*"},
    {"IS_ALPHA": True, "OP": "?"},
]

# TODO: We can probably combine some of these patterns, e.g. NCT|DRKS|ISRCTN
# ClinicalTrials.gov
NCT_PATTERN_1 = [{'TEXT': {"REGEX": "^NCT[-\u2010-\u2013/]?[0-9]{8}(?=[.,:;)]|$)"}}]
NCT_PATTERN_2 = [{'ORTH': "NCT"},
                 {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                 {'TEXT': {"REGEX": "^[0-9]{8}(?=[.,:;)]|$)"}}]
NCT_PATTERN_3 = [{'ORTH': "NCT"},
                 {'TEXT': {"REGEX": "^(#|[Nn]o|[Nn]um(ber)?)$"}},
                 {'ORTH': ":", "OP": "?"},
                 {'TEXT': {"REGEX": "^[0-9]{8}(?=[.,:;)]|$)"}, "OP": "?"}
                 ]

# ANZCTR:
ANZ_PATTERN_1 = [{'TEXT': {"REGEX": "^ACTRN[-\u2010-\u2013/]?[0-9]{14}(?=[.,:;)]|$)"}}]
ANZ_PATTERN_2 = [{'ORTH': "ACTRN", "OP": "?"}, {'TEXT': {"REGEX": "^126[0-9]{11}(?=[.,:;)]|$)"}}]
ANZ_PATTERN_3 = [{'ORTH': "ACTRN"},
                 {'TEXT': {"REGEX": "^(#|[Nn]o|[Nn]um(ber)?)$"}},
                 {'ORTH': ":", "OP": "?"},
                 {'TEXT': {"REGEX": "^[0-9]{14}(?=[.,:;)]|$)"}, "OP": "?"}
                 ]

# Universal trial number
# U1111-1254-7316
UTN_PATTERN = [{'TEXT': {"REGEX": "^U[0-9]{4}[-\u2010-\u2013/]?[0-9]{4}[-\u2010-\u2013/]?[0-9]{4}(?=[.,:;)]|$)"}}]

# DRKS
# DRKS00000002
DRKS_PATTERN_1 = [{'TEXT': {"REGEX": "^DRKS[-\u2010-\u2013/]?[0-9]{8}(?=[.,:;)]|$)"}}]
DRKS_PATTERN_2 = [{'ORTH': "DRKS"},
                  {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                  {'TEXT': {"REGEX": "^[0-9]{8}(?=[.,:;)]|$)"}}]
DRKS_PATTERN_3 = [{'ORTH': "DRKS"},
                  {'TEXT': {"REGEX": "^(#|[Nn]o|[Nn]um(ber)?)$"}},
                  {'ORTH': ":", "OP": "?"},
                  {'TEXT': {"REGEX": "^[0-9]{8}(?=[.,:;)]|$)"}, "OP": "?"}
                  ]

# ISRCTN
# ISRCTN14702259
ISRCTN_PATTERN_1 = [{'TEXT': {"REGEX": "^ISRCTN[-\u2010-\u2013/]?[0-9]{8}(?=[.,:;)]|$)"}}]
ISRCTN_PATTERN_2 = [{'ORTH': "ISRCTN"},
                    {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                    {'TEXT': {"REGEX": "^[0-9]{8}(?=[.,:;)]|$)"}}]
ISRCTN_PATTERN_3 = [{'ORTH': "ISRCTN"},
                    {'TEXT': {"REGEX": "^(#|[Nn]o|[Nn]um(ber)?)$"}},
                    {'ORTH': ":", "OP": "?"},
                    {'TEXT': {"REGEX": "^[0-9]{8}(?=[.,:;)]|$)"}, "OP": "?"}
                    ]

# CRD
# CRD42020179519
# https://www.crd.york.ac.uk/prospero/display_record.php?RecordID=179519
CRD_PATTERN_1 = [{'TEXT': {"REGEX": "^CRD[-\u2010-\u2013/]?[0-9]{11}(?=[.,:;)]|$)"}}]
CRD_PATTERN_2 = [{'ORTH': "CRD"},
                 {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                 {'TEXT': {"REGEX": "^[0-9]{11}(?=[.,:;)]|$)"}}]
CRD_PATTERN_3 = [{'ORTH': "CRD"},
                 {'TEXT': {"REGEX": "^(#|[Nn]o|[Nn]um(ber)?)$"}},
                 {'ORTH': ":", "OP": "?"},
                 {'TEXT': {"REGEX": "^[0-9]{11}(?=[.,:;)]|$)"}, "OP": "?"}
                 ]

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
JPRN_PATTERN_4 = [{'ORTH': "JPRN"},
                  {'TEXT': {"REGEX": "^(#|[Nn]o|[Nn]um(ber)?)$"}},
                  {'ORTH': ":", "OP": "?"},
                  {'TEXT': {"REGEX": "^[0-9]{9}(?=[.,:;)]|$)"}, "OP": "?"}
                  ]

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
CHICTR_PATTERN_4 = [{'ORTH': "ChiCTR"},
                    {'TEXT': {"REGEX": "^(#|[Nn]o|[Nn]um(ber)?)$"}},
                    {'ORTH': ":", "OP": "?"},
                    {'TEXT': {"REGEX": "^[0-9]{8,10}(?=[.,:;)]|$)"}, "OP": "?"}
                    ]

# PACTR
# PACTR202008685699453
# https://apps.who.int/trialsearch/Trial2.aspx?TrialID=PACTR202008685699453
PACTR_PATTERN_1 = [{'TEXT': {"REGEX": "^PACTR[-\u2010-\u2013/]?[0-9]{15}(?=[.,:;)]|$)"}}]
PACTR_PATTERN_2 = [{'ORTH': "PACTR"},
                   {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                   {'TEXT': {"REGEX": "^[0-9]{15}(?=[.,:;)]|$)"}}]
PACTR_PATTERN_3 = [{'ORTH': "PACTR"},
                   {'TEXT': {"REGEX": "^(#|[Nn]o|[Nn]um(ber)?)$"}},
                   {'ORTH': ":", "OP": "?"},
                   {'TEXT': {"REGEX": "^[0-9]{15}(?=[.,:;)]|$)"}, "OP": "?"}
                   ]

# KCT
# KCT0005285
# https://apps.who.int/trialsearch/Trial2.aspx?TrialID=KCT0005285
KCT_PATTERN_1 = [{'TEXT': {"REGEX": "^KCT[-\u2010-\u2013/]?[0-9]{7}(?=[.,:;)]|$)$"}}]
KCT_PATTERN_2 = [{'ORTH': "KCT"},
                 {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                 {'TEXT': {"REGEX": "^[0-9]{7}(?=[.,:;)]|$)$"}}]
KCT_PATTERN_3 = [{'ORTH': "KCT"},
                 {'TEXT': {"REGEX": "^(#|[Nn]o|[Nn]um(ber)?)$"}},
                 {'ORTH': ":", "OP": "?"},
                 {'TEXT': {"REGEX": "^[0-9]{7}(?=[.,:;)]|$)"}, "OP": "?"}
                 ]

# https://aspredicted.org/
ASP_PATTERN = [{'TEXT': {"REGEX": "^https?://aspredicted.org/.+$"}}]

# EudraCT
# https://www.clinicaltrialsregister.eu/ctr-search/search?query=covid-19
EUDRACT_PATTERN_1 = [{'TEXT': {"REGEX": "^EudraCT$"}},
                     {'TEXT': {"REGEX": "^(#|[Nn]o|[Nn]um(ber)?)$"}},
                     {'ORTH': ":", "OP": "?"},
                     {'TEXT': {"REGEX": "^[0-9]{4}$"}},
                     {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                     {'TEXT': {"REGEX": "^[0-9]{6}$"}},
                     {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                     {'TEXT': {"REGEX": "^[0-9]{2}$"}}
                     ]
EUDRACT_PATTERN_2 = [{'TEXT': {"REGEX": "^EudraCT#[0-9]{4}$"}},
                     {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                     {'TEXT': {"REGEX": "^[0-9]{6}$"}},
                     {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                     {'TEXT': {"REGEX": "^[0-9]{2}$"}}
                     ]

GENERAL_PREREG_PATTERN = [{'TEXT': {"REGEX": "^[Pp]re$"}, "OP": "?"},
                          {'TEXT': {"REGEX": "[-\u2010-\u2013/]"}, "OP": "?"},
                          {'TEXT': {"REGEX": "^([Pp]re)?[Rr]egist(ered|ration)$"}},
                          {"IS_ALPHA": True, "OP": "?"},
                          {"IS_ALPHA": True, "OP": "?"},
                          {"IS_ALPHA": True, "OP": "?"},
                          {'TEXT': {"REGEX": "^(at|from|:)$"}},
                          {'ORTH': ":", "OP": "?"},
                          {'TEXT': {"REGEX": "^https?://.+$"}}
                          ]


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
        {"label": TRIAL_LABEL, "pattern": NCT_PATTERN_3},
        {"label": TRIAL_LABEL, "pattern": ANZ_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": ANZ_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": ANZ_PATTERN_3},
        {"label": TRIAL_LABEL, "pattern": UTN_PATTERN},
        {"label": TRIAL_LABEL, "pattern": DRKS_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": DRKS_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": DRKS_PATTERN_3},
        {"label": TRIAL_LABEL, "pattern": ISRCTN_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": ISRCTN_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": ISRCTN_PATTERN_3},
        {"label": TRIAL_LABEL, "pattern": CRD_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": CRD_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": CRD_PATTERN_3},
        {"label": TRIAL_LABEL, "pattern": JPRN_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": JPRN_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": JPRN_PATTERN_3},
        {"label": TRIAL_LABEL, "pattern": JPRN_PATTERN_4},
        {"label": TRIAL_LABEL, "pattern": CHICTR_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": CHICTR_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": CHICTR_PATTERN_3},
        {"label": TRIAL_LABEL, "pattern": CHICTR_PATTERN_4},
        {"label": TRIAL_LABEL, "pattern": PACTR_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": PACTR_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": PACTR_PATTERN_3},
        {"label": TRIAL_LABEL, "pattern": KCT_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": KCT_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": KCT_PATTERN_3},
        {"label": TRIAL_LABEL, "pattern": ASP_PATTERN},
        {"label": TRIAL_LABEL, "pattern": EUDRACT_PATTERN_1},
        {"label": TRIAL_LABEL, "pattern": EUDRACT_PATTERN_2},
        {"label": TRIAL_LABEL, "pattern": GENERAL_PREREG_PATTERN},
        {"label": DATA_AVAILABILITY_LABEL_URL, "pattern": DATA_AVAILABILITY_PATTERN_URL},
        {"label": DATA_AVAILABILITY_LABEL_CLOSED, "pattern": DATA_AVAILABILITY_PATTERN_CLOSED},
        {"label": DATA_AVAILABILITY_LABEL_SUPPL, "pattern": DATA_AVAILABILITY_PATTERN_SUPPLEMENT},
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
    entity_data = []
    for sent in doc.sents:
        for ent in sent.ents:
            if ent:
                entity_data.append({'sentence': sent, 'entity': ent.text, 'label': ent.label_})
                print(sent, ent.text, ent.label_)
    return entity_data


if __name__ == "__main__":
    args = sys.argv
    main(args[1])
