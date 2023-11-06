from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

import numpy as np

from sklearn.model_selection import cross_validate
from root.classifiers.utils import check_data, get_X_Y

METRICS = {
    'accuracy':     'accuracy',
    'precision':    'precision',
    'recall':       'recall',
    'auc':          'roc_auc',
    'f1':           'f1',
}

# BALANCED_TRAINING one of 'balanced', 'balanced_subsample', 'None'

class Tree:
    def __init__(self, algorithm = 'RF-G-150', BALANCED_TRAINING='balanced'):
        if 'RF' in algorithm:
            criterion = algorithm.split('-')[1]
            n_estimators = int(algorithm.split('-')[2])
            if criterion=='E':
                self.model = RandomForestClassifier(n_estimators=n_estimators, criterion='entropy', class_weight=BALANCED_TRAINING)
            else:
                self.model = RandomForestClassifier(n_estimators=n_estimators, criterion='gini', class_weight=BALANCED_TRAINING)
        elif algorithm == 'GNB':
            self.model = GaussianNB()
        elif algorithm == 'KNN':
            self.model = KNeighborsClassifier(3)
        elif algorithm == 'SVC':
            self.model = SVC()
        elif algorithm == 'DT-G':
            self.model = DecisionTreeClassifier(criterion="gini", class_weight=BALANCED_TRAINING)
        elif algorithm == 'DT-E':
            self.model = DecisionTreeClassifier(criterion="entropy", class_weight=BALANCED_TRAINING)
        else:
            raise NotImplementedError('Classifier algorithm {} not implemented'.format(algorithm))

    def kfold(self, data_manager):

        X, y = get_X_Y(data_manager)
        check_data(X, y)

        k = 10

        scores = cross_validate(self.model, X, y, cv=k, scoring=METRICS)

        out = {
            'accuracy':  np.mean(scores['test_accuracy']),
            'precision': np.mean(scores['test_precision']),
            'recall':    np.mean(scores['test_recall']),
            'auc':       np.mean(scores['test_auc']),
            'f1':        np.mean(scores['test_f1']),
        }

        return out['auc']
