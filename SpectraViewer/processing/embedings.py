from matplotlib import offsetbox
from sklearn import (manifold, decomposition, ensemble,
                     discriminant_analysis, random_projection)
import numpy as np

def get_embedding(X,y,type_embeding):
    
    n_neighbors = 30   
    X_projected = None
    
    if type_embeding=="Random":
        rp = random_projection.SparseRandomProjection(n_components=2, random_state=42)
        X_projected = rp.fit_transform(X)
        
    elif type_embeding=="PCA":
        X_projected = decomposition.TruncatedSVD(n_components=2).fit_transform(X)
        
    elif type_embeding=="LDA":
        X2 = X.copy()
        X2.flat[::X.shape[1] + 1] += 0.01  # Make X invertible
        X_projected = discriminant_analysis.LinearDiscriminantAnalysis(n_components=2).fit_transform(X2, y)
        
    elif type_embeding=="Isomap":
        X_projected = manifold.Isomap(n_neighbors, n_components=2).fit_transform(X)
    
    elif type_embeding=="LLE":
        clf = manifold.LocallyLinearEmbedding(n_neighbors, n_components=2,
                                      method='standard')
        X_projected = clf.fit_transform(X)
        
    elif type_embeding=="mLLE":
        clf = manifold.LocallyLinearEmbedding(n_neighbors, n_components=2,
                                      method='modified')
        X_projected = clf.fit_transform(X)
        
    elif type_embeding=="hLLE":
        clf = manifold.LocallyLinearEmbedding(n_neighbors, n_components=2,
                                      method='hessian')
        X_projected = clf.fit_transform(X)
    
    elif type_embeding=="ltsa":
        clf = manifold.LocallyLinearEmbedding(n_neighbors, n_components=2,
                                      method='ltsa')
        X_projected = clf.fit_transform(X)
        
    elif type_embeding=="MDS":
        clf = manifold.MDS(n_components=2, n_init=1, max_iter=100)
        X_projected = clf.fit_transform(X)
        
    elif type_embeding=="RF":
        hasher = ensemble.RandomTreesEmbedding(n_estimators=200, random_state=0,
                                       max_depth=5)
        
        X_transformed = hasher.fit_transform(X)
        pca = decomposition.TruncatedSVD(n_components=2)
        X_projected = pca.fit_transform(X_transformed)
    
    elif type_embeding=="Spectral":
        embedder = manifold.SpectralEmbedding(n_components=2, random_state=0,
                                      eigen_solver="arpack")
        X_projected = embedder.fit_transform(X)
        
    elif type_embeding=="T-SNE":
        tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
        X_projected = tsne.fit_transform(X)
    else:
        print("""Valid options are:
         Random    => Random Projections
         PCA       => Principal Component Analysis
         LDA       => Linear Discriminant Analysis
         Isomap    => Isomap
         LLE       => Locally Linear Embedding
         mLLE      => Modified Locally Linear Embedding
         hLLE      => Hessian Locally Linear Embedding
         ltsa      => Locally Linear Embedding (ltsa)
         MDS       => Multidimensional Scaling
         RF        => Random Forest Embeding
         Spectral  => Spectral Embeding
         T-SNE     => T-SNE    """)
    
    return X_projected
        


types = ["Random","PCA","LDA", "Isomap","LLE","mLLE",
         "hLLE","ltsa","MDS","RF","Spectral","T-SNE"]