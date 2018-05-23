import numpy as np
from sklearn.metrics import pairwise_distances


def get_intraExtra_distance_matrix(X, y, classNames, metric):
    n_classes = len(classNames)
    avg_dist = np.zeros((n_classes, n_classes))

    for i in range(n_classes):
        for j in range(n_classes):
            avg_dist[i, j] = pairwise_distances(X[y == classNames[i]],
                                                X[y == classNames[j]],
                                                metric=metric).mean()
    avg_dist /= avg_dist.max()

    return avg_dist
