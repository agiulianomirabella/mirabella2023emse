import numpy as np
from sklearn.model_selection import cross_val_score

# for dataset with size lower than threhsold, the score is 0
THRESHOLD = 10

def compute_scores(predictor, X_train, y_train):

    # compute number of valid and faulty requests
    n_valid  = y_train.tolist().count(True)
    n_faulty = y_train.tolist().count(False)
    n_minority = min(n_valid, n_faulty)
    
    if n_valid + n_faulty < THRESHOLD:
        return 0, 0

    if n_minority < 1:
        return 0, 0

    # compute the number of folds
    n_folds = min(5, n_minority)

    # compute the metrics
    accuracy = np.mean(cross_val_score(predictor, X_train, y_train, cv=n_folds, scoring='accuracy'))
    roc_auc  = np.mean(cross_val_score(predictor, X_train, y_train, cv=n_folds, scoring='roc_auc'))

    return accuracy, roc_auc


