from unittest import TestCase

from main import main


class TestPatterns(TestCase):
    def test_extract_data_availability(self):
        text = 'Supplementary data is available from the author'
        output = main(text)
        self.assertEquals(output[0].get('label'), 'DATA_AVAILABILITY_CLOSED')

    def test_extract_data_availability_1(self):
        text = "Anonymised, patient level data are available from the corresponding author upon request, " \
               "subject to submission of a suitable study protocol and analysis plan"
        output = main(text)
        self.assertEquals(output[0].get('label'), 'DATA_AVAILABILITY_CLOSED')

    def test_extract_data_availability_2(self):
        text = "The computer code used in this study is available from the authors upon request"
        output = main(text)
        self.assertEquals(output[0].get('label'), 'DATA_AVAILABILITY_CLOSED')

    def test_extract_data_availability_3(self):
        text = "Our source code is available at goo.gl/TXBp4e"
        output = main(text)
        self.assertEquals(output[0].get('label'), 'DATA_AVAILABILITY_OPEN_URL')

    def test_extract_data_availability_4(self):
        text = "Supplementary Data are available at IJE online"
        output = main(text)
        self.assertEquals(output[0].get('label'), 'DATA_AVAILABILITY_OPEN_SUPPLEMENT')

    def test_extract_data_availability_5(self):
        text = "Crystallographic data that support the findings of this study have been deposited in the Protein " \
               "Data Bank with the accession codes 5TSG and 5TSH"
        output = main(text)
        self.assertEquals(output[0].get('label'), 'DATA_AVAILABILITY_OPEN_SUPPLEMENT')

    def test_extract_data_availability_6(self):
        text = "The code to reproduce our experimental setup is provided at " \
               "https://github.com/google-research/google-research/tree/master/summae"
        output = main(text)
        self.assertEquals(output[0].get('label'), 'DATA_AVAILABILITY_OPEN_URL')

    def test_extract_data_availability_7(self):
        text = 'Supplementary data is available on the publisher\u2019s web-site'
        output = main(text)
        entity_label = output[0].get('label')
        entity_text = output[0].get('entity')
        self.assertEquals(entity_text, 'Supplementary data is available on the publisher\u2019s web-site')
        self.assertEquals(entity_label, 'DATA_AVAILABILITY_OPEN_SUPPLEMENT')

    def test_extract_data_availability_8(self):
        text = 'Supplementary data is available in Appendices I\u2013L'
        output = main(text)
        entity_label = output[0].get('label')
        entity_text = output[0].get('entity')
        self.assertEquals(entity_text, 'Supplementary data is available in Appendices I\u2013L')
        self.assertEquals(entity_label, 'DATA_AVAILABILITY_OPEN_SUPPLEMENT')

    def test_extract_data_availability_9(self):
        text = 'Supplementary data is available in Appendix 1, and figures can be obtained separately'
        output = main(text)
        entity_label = output[0].get('label')
        entity_text = output[0].get('entity')
        self.assertEquals(entity_text, 'Supplementary data is available in Appendix 1')
        self.assertEquals(entity_label, 'DATA_AVAILABILITY_OPEN_SUPPLEMENT')

    def test_extract_trial_registration(self):
        text = "The trial is registeredwith the Australian and New Zealand Clinical " \
               "TrialsRegistry (ACTRN 12612000026820)."
        output = main(text)
        self.assertEquals(output[0].get('label'), 'TRIAL_REGISTRATION_ID')

    def test_extract_trial_registration_1(self):
        text = "registered on the internal standardised randomised controlled trial " \
               "register (ISRCTN no. 90464927)"
        output = main(text)
        self.assertEquals(output[0].get('label'), 'TRIAL_REGISTRATION_ID')

    def test_extract_trial_registration_2(self):
        text = "European Clinical Trial Registry, EudraCT#2016-000891-54."
        output = main(text)
        self.assertEquals(output[0].get('label'), 'TRIAL_REGISTRATION_ID')

    def test_extract_trial_registration_3(self):
        text = "European Clinical Trial Registry, EudraCT #2016-000891-54."
        output = main(text)
        self.assertEquals(output[0].get('label'), 'TRIAL_REGISTRATION_ID')

    def test_extract_trial_registration_4(self):
        text = "EudraCT Number: 2018-001516-30"
        output = main(text)
        self.assertEquals(output[0].get('label'), 'TRIAL_REGISTRATION_ID')

    def test_extract_trial_registration_5(self):
        text = "study was pre-registered at https://osf.io/abcsd"
        output = main(text)
        self.assertEquals(output[0].get('label'), 'TRIAL_REGISTRATION_ID')

    def test_extract_trial_registration_6(self):
        text = "Trial registration: https://osf.io/abcsd"
        output = main(text)
        self.assertEquals(output[0].get('label'), 'TRIAL_REGISTRATION_ID')

    def test_extract_trial_registration_7(self):
        text = "The current study was preregistered on the Open Science Framework. " \
               "The preregistration documents are available at https://osf.io/abcsd"
        output = main(text)
        self.assertEquals(output[0].get('label'), 'TRIAL_REGISTRATION_ID')

