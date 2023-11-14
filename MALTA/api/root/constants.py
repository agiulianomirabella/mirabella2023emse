import os
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier

from sklearn.preprocessing import MinMaxScaler

# PREDICTOR = RandomForestClassifier(n_estimators=300, criterion='gini', class_weight='balanced_subsample')
PREDICTOR = RandomForestClassifier(n_estimators=300, criterion='gini')
SCALER = MinMaxScaler()

DEFAULT_RESAMPLING_RATIO = 1

RESTEST_PATH = '../RESTest/'
