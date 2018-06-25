import unittest
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from SpectraViewer.models import Dataset, ClassifierSet, Spectrum


class ModelsTest(unittest.TestCase):

    def test_dataser(self):
        df = pd.DataFrame(np.random.randint(0, 10, size=(10, 10)))
        name = 'name'
        user = '00000'
        notes = 'notes'
        dataset = Dataset(name, user, df.to_json(orient='split'), notes)
        self.assertEqual(dataset.name, name)
        self.assertEqual(dataset.user, user)
        self.assertTrue(df.equals(pd.read_json(dataset.data, orient='split')))
        self.assertEqual(dataset.notes, notes)

    def test_spectrum(self):
        df = pd.DataFrame(np.random.randint(0, 10, size=(10, 10)))
        name = 'name'
        user = '00000'
        notes = 'notes'
        spectrum = Spectrum(name, user, df.to_json(orient='split'), notes)
        self.assertEqual(spectrum.name, name)
        self.assertEqual(spectrum.user, user)
        self.assertTrue(df.equals(pd.read_json(spectrum.data, orient='split')))
        self.assertEqual(spectrum.notes, notes)

    def test_classifier(self):
        name = 'name'
        user = '00000'
        notes = 'notes'
        mine = LogisticRegression(C=1.0)
        prof = LogisticRegression(C=2.0)
        pnum = LogisticRegression(C=3.0)
        classifiers = ClassifierSet(name, user, notes, mine, prof, pnum)
        self.assertEqual(classifiers.name, name)
        self.assertEqual(classifiers.user, user)
        self.assertEqual(classifiers.notes, notes)
        self.assertEqual(classifiers.mine, mine)
        self.assertEqual(classifiers.prof, prof)
        self.assertEqual(classifiers.pnum, pnum)
