import pandas as pd
import numpy as np
import random

import os
import glob

'''

'''
def get_spectrum_data(path, interpolate = True):
    '''
    Hace interpolación lineal con numpy, 
    
    import numpy as np

    xp = [1, 2, 3]
    fp = [3, 2, 0]
    np.interp(2.5, xp, fp)


    ys = np.interp([0, 1, 1.5, 2, 2.5, 3], xp, fp)

    ys   
    
    
    podría hacerla cuadratica así:
    
    import math
    from scipy import interpolate

    f = interpolate.interp1d(xp, fp, 
                             kind ="quadratic",
                             bounds_error=False)
    ys2= f([0, 1, 1.5, 2, 2.5, 3]) 

    if math.isnan(ys2[0]):
        ys2[0] = ys2[1]
    
    ys2    
    
    '''
    X = [] # datos 
    y = [] # clases
    feature_names = None
    files = []
    
    if interpolate:
        feature_names = np.arange(50,2801)
        
    
    classes = [name for name in os.listdir(path) 
               if os.path.isdir(os.path.join(path, name))]
    
    paths = dict()

    for cl in classes: 
        current_paths=sorted(glob.glob(os.path.join(path,cl,"*.CSV")))
        paths[cl]=current_paths
        
    
    for cl in classes: # por cada clase
        csv_paths=paths[cl]
        for path in csv_paths:
            data = pd.read_csv(path,sep=";",header=None)
            values = data[1].values
            
            #algunos spectogramas empiezan por 0 
            # preguntar
            if values[0]==0:
                values[0]=values[1]
                
            if interpolate:
                oldx = data[0].values # aquí habría que sumar algo en función del path, para calibrar
                values = np.interp(feature_names, oldx, values)
            
        
            if feature_names is None:
                feature_names = data[0].round(1).values
            
            X.append(values[:2800]) #cojo las 2800 primeras, porque sin interpolate podrían ser mas
            y.append(cl.replace(" ","")) #elimina espacios
            files.append(path)
    return  np.vstack(X), np.array(y),feature_names[:2800], files
    
