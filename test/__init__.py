from unittest import TestCase

from main import main


class TestPatterns(TestCase):
    def test_data_availability(self):
        text = 'Supplementary data is available from the author'
        output = main(text)
        self.assertEquals(output[0].get('label'), 'DATA_AVAILABILITY')

    def test_extract_data_availability_1(self):
        text = "Anonymised, patient level data are available from the corresponding author upon request, " \
               "subject to submission of a suitable study protocol and analysis plan"
        output = main(text)
        self.assertEquals(output[0].get('label'), 'DATA_AVAILABILITY')

    def test_extract_data_availability_2(self):
        text = "The computer code used in this study is available from the authors upon request"
        output = main(text)
        self.assertEquals(output[0].get('label'), 'DATA_AVAILABILITY')

    def test_extract_data_availability_3(self):
        text = "Our source code is available at goo.gl/TXBp4e"
        output = main(text)
        self.assertEquals(output[0].get('label'), 'DATA_AVAILABILITY')

    def test_extract_data_availability_4(self):
        text = "Supplementary Data are available at IJE online"
        output = main(text)
        self.assertEquals(output[0].get('label'), 'DATA_AVAILABILITY')

    def test_extract_data_availability_5(self):
        text = "Crystallographic data that support the findings of this study have been deposited in the Protein " \
               "Data Bank with the accession codes 5TSG and 5TSH"
        output = main(text)
        self.assertEquals(output[0].get('label'), 'DATA_AVAILABILITY')

    def test_extract_data_availability_6(self):
        text = "The code to reproduce our experimental setup is provided at " \
               "https://github.com/google-research/google-research/tree/master/summae"
        output = main(text)
        self.assertEquals(output[0].get('label'), 'DATA_AVAILABILITY')

    def test_extract_trial_registration(self):
        text = "The trial is registeredwith the Australian and New Zealand Clinical " \
               "TrialsRegistry (ACTRN 12612000026820)."
        output = main(text)
        self.assertEquals(output[0].get('label'), 'TRIAL_REGISTRATION_ID')
