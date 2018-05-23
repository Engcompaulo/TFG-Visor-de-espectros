import warnings
warnings.filterwarnings("ignore")

import pandas as pd

from sklearn.model_selection import cross_val_score



from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_predict

from sklearn.feature_selection import SelectFromModel


def get_best_att(clf,X,y, threshold=0.25):
    # Set a minimum threshold of 0.25
    sfm = SelectFromModel(clf, threshold=threshold)    
   
    sfm.fit(X, y)
    # Obtención de los atributos seleccionados a partir del modelo y el threshold
    support=sfm.get_support(indices=False) #suport son Trues y Falses
    selected = sfm.transform(X)
    
    print(selected.shape)
    
    return support,selected

# al menos con Regresión logistica
def get_cls_weights(cls, X,y):
    
    cls.fit(X,y)
    
    if hasattr(cls, 'coef_'):
        pesos =abs(cls.coef_)[0]
    elif hasattr(cls, 'feature_importances_'):
        pesos = cls.feature_importances_
        
        
    return pesos



# a experiments
def get_xval_confusion_matrix(numFolds,model,X,y):
    preds = cross_val_predict(model, X, y, cv=numFolds)
    cnf_matrix = confusion_matrix(y, preds)
    return cnf_matrix


def get_xval_models_problems_atts(numFolds,models,problems,att_reprs):
    results = []
    classifierDesc = []
    problemDesc = []
    attDesc = []
    
    att_reprs_names = list(att_reprs.keys())
    problem_names = list(problems.keys())


    for i in range(len(problem_names)):
        for j in range(len(att_reprs_names)):
            problem_name = problem_names[i]
            atts_name = att_reprs_names[j]
            classes = problems[problem_name]
            X = att_reprs[atts_name]

            for name_cls, model in models:

                cv_results = cross_val_score(model, X, classes, cv=numFolds, scoring='accuracy').mean()
                #print(problem_name,name_cls,cv_results)
                results.append(cv_results) 
                classifierDesc.append(name_cls)
                problemDesc.append(problem_name)
                attDesc.append(atts_name)


    dfResults = pd.DataFrame({"Class":problemDesc,
                              "attDesc":attDesc,
                              "Clasificador":classifierDesc, 
                              "Media": results})
    
    return dfResults
