from .BaselineCorrection import BaselineCorrection
from .superman.preprocess import preprocess
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from scipy.signal import wiener

'''
Preprocess implementa BaseEstimator y TransformerMixin

Un estimador es la clase básica de sklearn y un transformer tiene los metodos transform y fit_transform

class sklearn.base.BaseEstimator Base class for all estimators in scikit-learn
class sklearn.base.TransformerMixin Mixin class for all transformers in scikit-learn.


    normalize:
        - max divide por el máximo
        - min resta el mínimo
        - band XXX no está implementado
        - cum Cumulative intensity normalization method.
              "Quality Assessment of Tandem Mass Spectra Based on
               Cumulative Intensity Normalization", Na & Paek, J. of Proteome Research
        - norm3 XXX no esta implementado
        - l1 y l2 sklearn.preprocessing.normalize y=x/z
            z es sumatorio de valores absolutos en l1
            z es raiz de sumatorio cuadrados en l1
        - norm (propia) resta min y divide por rango
        
     squashing 
        - sqrt
        - cos
            
     smooth y deriv
        Savitzky-Golay con orden 0 o 1
        wiener
        



'''


class PreprocessOperator(BaseEstimator, TransformerMixin):
    # es en el init donde me llegan las opciones de lo que voy a tener que hacer
    '''
    Utiliza un argumento de tipo diccionario
    
    
    def test(args, **kwargs):
        print(args,kwargs)
    
    test(1, a=3, b=4)
    => 1 {'a': 3, 'b': 4}
    
    '''

    def __init__(self, op_type, **op_params):

        self.feature_names = []
        self.op_type = op_type
        self.op_params = op_params
        if op_type == 'crop':
            self.feature_names = op_params["feature_names"]

    def get_feature_names(self):
        return self.feature_names

    def fit(self, x, y=None):
        return self

    def transform(self, data):
        return self.preprocess(data)

    def get_options(self):
        # None al principio para que sea opcion por defecto

        return {
            'normalize': {"type": ['l1', 'l2', 'cum', 'min', 'max', 'norm']},
            'squash': {"type": ['sqrt', 'cos']},
            'smooth': {"type": ['sg', 'wiener']},
            'deriv': {},
            'crop': {'feature_names': None,
                     'orig': (50, 2000),
                     'end': (50, 2000)}
            }

    def preprocess(self, data):

        superman_normalizations = ['l1', 'l2', 'cum', 'min', 'max']
        options_str = ""

        if self.op_type == "normalize":
            normalize_type = self.op_params["type"]
            if normalize_type in superman_normalizations:
                options_str = 'normalize:' + normalize_type
            elif normalize_type == 'norm':
                m = data.min(axis=1)
                r = data.ptp(axis=1)

                data = ((data.transpose() - m) / r).transpose()
        elif self.op_type == 'squash':
            squash_type = self.op_params["type"]

            if squash_type is not None:
                options_str = 'squash:' + squash_type

        elif self.op_type == 'smooth':
            smooth_type = self.op_params["type"]
            size = self.op_params["size"]
            if smooth_type == "sg":
                options_str = 'smooth:' + str(size) + ':2'
            else:  # case wiener
                data = wiener(data, (1, size))

        elif self.op_type == 'deriv':
            options_str = 'deriv:3:1'

        elif self.op_type == 'crop':
            att_names = self.feature_names
            ori = self.op_params["ori"]
            end = self.op_params["end"]

            i = 0
            while att_names[i] < ori:
                i += 1
            new_ori = i

            i = len(att_names) - 1
            while att_names[i] > end:
                i -= 1

            new_end = i

            att_names = att_names[new_ori:new_end]
            data = data[:, new_ori:new_end]
            self.feature_names = att_names

        if options_str != "":
            data = preprocess(data, options_str)

        return data


class PreprocessPipeline(BaseEstimator, TransformerMixin):

    def __init__(self, att_names, orden, ori=50, end=1800, baseline='ALS_old',
                 normalize="norm", squash="cos", smooth_type='sg',
                 smooth_size=25):
        self.att_names = att_names
        self.orden = orden
        self.ori = ori
        self.end = end
        self.baseline = baseline
        self.normalize = normalize
        self.squash = squash
        self.smooth_size = smooth_size
        self.pipe = None

        steps = []

        tipoOp_id = {'C': 0, 'B': 0, 'N': 0, 'S': 0, 's': 0, 'd': 0}

        for op in orden:
            tipoOp_id[op] += 1
            if op == 'C' and ori < end:
                steps.append(("Crop" + str(tipoOp_id[op]),
                              PreprocessOperator("crop",
                                                 feature_names=att_names,
                                                 ori=ori, end=end)))

            if op == 'B':
                steps.append(("Baseline" + str(tipoOp_id[op]),
                              BaselineCorrection(baseline)))

            if op == 'N':
                steps.append(("Normalize" + str(tipoOp_id[op]),
                              PreprocessOperator("normalize", type=normalize)))

            if op == 'S':
                steps.append(("Squashing" + str(tipoOp_id[op]),
                              PreprocessOperator("squash", type=squash)))

            if op == 's':
                steps.append(("Smoothing" + str(tipoOp_id[op]),
                              PreprocessOperator("smooth", type=smooth_type,
                                                 size=smooth_size)))

            if op == 'd':
                steps.append(("Derive" + str(tipoOp_id[op]),
                              PreprocessOperator("deriv")))

        if len(steps) > 0:
            self.pipe = Pipeline(steps)

    def get_pipeline(self):
        return self.pipe

    def get_att_names(self):
        return self.att_names

    def fit(self, x, y=None):
        return self

    def transform(self, data):

        if self.pipe is not None:
            data = self.pipe.transform(data)

            cropStep = None
            for step in self.pipe.steps:
                if "Crop" in step[0]:
                    cropStep = step[1]

            if cropStep is not None:
                self.att_names = cropStep.get_feature_names()

        return data


def preprocess_pipeline(X, att_names, orden, ori, end, baseline, normalize,
                        squash, smooth_type, smooth_s):
    pp = PreprocessPipeline(att_names, orden, ori, end, baseline, normalize,
                            squash, smooth_type, smooth_s)
    X = pp.transform(X)
    att_names = pp.get_att_names()

    return X, att_names
