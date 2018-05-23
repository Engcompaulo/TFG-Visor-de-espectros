import numpy as np
import math

from sklearn.base import BaseEstimator, TransformerMixin

'''
IntervalFeatures implementa BaseEstimator y TransformerMixin

Un estimador es la clase básica de sklearn y un transformer tiene los metodos transform y fit_transform

class sklearn.base.BaseEstimator Base class for all estimators in scikit-learn
class sklearn.base.TransformerMixin Mixin class for all transformers in scikit-learn.



'''


class IntervalFeatures(BaseEstimator, TransformerMixin):

    def __init__(self, attsNames, step_size=2, spec_size=200):
        self.names = attsNames
        self.step_size = step_size
        self.spec_size = spec_size

    def fit(self, x, y=None):
        return self

    def getFeatureNames(self):
        numValues = self.spec_size
        max_inter_size = math.ceil(math.log(numValues, 2))

        # progresión geométrica
        prog = np.logspace(0, max_inter_size, num=max_inter_size, base=2,
                           endpoint=False).astype(int)

        attsNames = []
        for n in prog[1:]:
            # print(n)
            for i in range(0, numValues - n + 1, self.step_size):
                interval = list(range(i, i + n))
                interval_name = str(self.names[interval[0]]) + "-" + str(
                    self.names[interval[-1]])

                attsNames.append(interval_name + "_min")
                attsNames.append(interval_name + "_max")
                attsNames.append(interval_name + "_range")
                attsNames.append(interval_name + "_mean")
                attsNames.append(interval_name + "_std")
        return attsNames

    def transform_one(self, values):
        numValues = self.spec_size
        max_inter_size = math.ceil(math.log(numValues, 2))

        # progresión geométrica
        prog = np.logspace(0, max_inter_size, num=max_inter_size, base=2,
                           endpoint=False).astype(int)

        attsValues = []
        for n in prog[1:]:
            # print(n)
            for i in range(0, numValues - n + 1, self.step_size):
                interval = list(range(i, i + n))
                interval_values = values[interval]

                attsValues.append(interval_values.min())
                attsValues.append(interval_values.max())
                attsValues.append(interval_values.ptp())
                attsValues.append(interval_values.mean())
                attsValues.append(interval_values.std())

        return attsValues

    def transform(self, X):
        return np.array([self.transform_one(x) for x in X])
