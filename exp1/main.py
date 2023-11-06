from root.data.utils import SERVICES
import numpy as np
import pandas as pd

from root.classifiers.mlp import MLP
from root.classifiers.trees import Tree
from root.data.manager import DataManager

ALGORITHMS = [
    'RF-G-50',
    'RF-G-100',
    'RF-G-150',
    'RF-G-200',
    'RF-G-250',
    'RF-G-300',
    'RF-G-350',
    'RF-G-400',

    'RF-E-50',
    'RF-E-100',
    'RF-E-150',
    'RF-E-200',
    'RF-E-250',
    'RF-E-300',
    'RF-E-350',
    'RF-E-400',

    'GNB', 
    'KNN', 
    'SVC', 
    'DT-G',
    'DT-E',
]

results = pd.DataFrame(index=ALGORITHMS, columns=SERVICES)

for service in SERVICES:
    data_manager = DataManager('data/' + service)
    data_manager.sample(frac=1)

    for algorithm in ALGORITHMS:
        clf = Tree(algorithm=algorithm)
        results.loc[algorithm, service] = np.mean(clf.kfold(data_manager))*100

    clf = MLP(len(list(data_manager.to_tree().columns)))
    results.loc['MLP', service] = np.mean(clf.kfold(data_manager))*100

results.loc[:, 'Mean'] = results.mean(axis=1)
results.loc[:, 'Std']  = results.std(axis=1)

results = results.sort_values(['Mean']).astype(float).T
results.to_csv('results.csv')