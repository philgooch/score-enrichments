import json
import spacy
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
from collections import defaultdict
import re

nlp = English()
ruler = EntityRuler(nlp)
ruler.from_disk("./data_patterns.jsonl")
ruler.from_disk("./registration_patterns.jsonl")
nlp.add_pipe(ruler)
nlp.add_pipe(nlp.create_pipe('sentencizer'))

nlp_registrations = spacy.load('../Trained models/Registrations')
nlp_data = spacy.load('../Trained models/Data')


for item in jsonl_list: #jsonl sentences
    sentence = json.loads(item)['text']

    ## First, apply the registration and data hard coded rules
    doc = nlp(sentence)
    if len(doc.ents) > 0:
        for ent in doc.ents:
            if ent.label_ == 'TRIAL_REGISTRATION_ID':
                registration_id += ent.text

    ## Next, apply the registration and data NLP models
    # Registrations
    with nlp_registrations.disable_pipes('ner'):
        doc = nlp_registrations(sentence)
    beams = nlp_registrations.entity.beam_parse([doc], beam_width=16, beam_density=0.0001)
    entity_scores = defaultdict(float)
    for beam in beams:
        for score, ents in nlp_registrations.entity.moves.get_beam_parses(beam):
            for start, end, label in ents:
                entity_scores[(start, end, label)] += score
    for key in entity_scores:
        start, end, label = key
        score = entity_scores[key]

        sanity = ["*", "[", "]", "(", ")", "=", "/", ".", ",", "+", "%", "§", ":", "·", "_"]
        if score == 1.0 and len(str(doc[start:end])) > 8 and not any(s in str(doc[start:end]).strip() for s in sanity) and not str(doc[start:end]).isalpha() and not str(doc[start:end]).isdigit() and not str(doc[start:end]).replace('-', '').isalpha() and re.match('^[\w-]+$', str(doc[start:end])) is not None:
            continue_exec = 'true'
            try:
                if len(str(doc[start:end]).strip().split(' ')[1]) == 4 and str(doc[start:end]).strip().split(' ')[1].isdigit():
                    continue_exec = 'false'
            except:
                continue_exec = 'true'

            if continue_exec == 'true' and label == 'TRIAL_REGISTRATION_ID':
                NLP_registration_id += str(doc[start:end])
                NLP_registration_score += str(score)
    # Data
    doc = nlp_data(sentence)
    sanity = ["data", "code", "software"]
    if any(s in str(sentence).lower() for s in sanity) and len(sentence) > 30 and len(sentence) < 300 and (doc.cats['DATA_AVAILABILITY_CLOSED'] > 0.99 or (doc.cats['DATA_AVAILABILITY_OPEN_URL'] > 0.80 and ('http' in sentence or 'www.' in sentence)) or doc.cats['DATA_AVAILABILITY_OPEN_SUPPLEMENT'] > 0.5):
        NLP_data_statement = sentence

        if doc.cats['DATA_AVAILABILITY_CLOSED'] > 0.99:
            NLP_data_statement_label += 'DATA_AVAILABILITY_CLOSED'
            NLP_data_score +=  str(doc.cats['DATA_AVAILABILITY_CLOSED'])
        elif doc.cats['DATA_AVAILABILITY_OPEN_URL'] > 0.80:
            NLP_data_statement_label +=  'DATA_AVAILABILITY_OPEN_URL'
            NLP_data_score += str(doc.cats['DATA_AVAILABILITY_OPEN_URL'])
        else:
            NLP_data_statement_label += 'DATA_AVAILABILITY_OPEN_SUPPLEMENT'
            NLP_data_score += str(doc.cats['DATA_AVAILABILITY_OPEN_SUPPLEMENT'])
