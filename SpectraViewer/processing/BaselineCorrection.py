from sklearn.base import BaseEstimator, TransformerMixin

from superman.baseline import BL_CLASSES
from baselines import BL_CLASSES_2

ALL_BL = {**BL_CLASSES, **BL_CLASSES_2}


import numpy as np

# TODO hallar una manera de pasar opciones a los métodos
# se crea la clase y luego se asignan parámetros
class BaselineCorrection (BaseEstimator, TransformerMixin):
    
    
    def __init__(self,bl_type):
        
        self.bl_type = bl_type
        
    
    
    def getOptions(self):
        keys = []
        options = []
        
        
        
        # por cada clase en el paquete tengo su nombre y su clase propiamente dicha
        for blr_key, blr_cls in ALL_BL.items():
            keys.append(blr_key)
            options.append(self.getBaselineOptions(blr_cls))
            
       
            
        return dict(zip(keys, options))
    
    def getBaselineOptions(self,blr_cls):
        bl = blr_cls()
        return bl.param_ranges()
    
    
    
    def fit(self, x, y=None):
        return self
    
    def transform(self, data):
        try:
            # trata de obtener la clase correspondiente a partir de la key
            blr_cls = ALL_BL[self.bl_type]
            bl = blr_cls()
            # aquí se asignarían parámetros

            bands = data.copy()


            #bands, intensities, segment=False, invert=False
            return bl.fit_transform(bands,data)

        except KeyError:
            # si no existe la key devuelve los datos sin procesar
            print("bl_type error")
            return data
        