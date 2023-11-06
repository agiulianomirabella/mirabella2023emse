import pandas as pd
from imblearn.over_sampling  import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler, EditedNearestNeighbours
from imblearn.combine        import SMOTEENN

def check_data(X, y):
    for data in [X, y]:
        if data.isnull().values.any():
            raise Exception('Something is wrong: empty value found in data.')
    if 'valid' in X.columns or 'exp_valid' in X.columns:
        raise Exception('Column valid or exp_valid found in data.')

def filter_X_columns(X, features_names):
    for column in X.columns:
        if not column in features_names:
            X = X.drop(column, axis=1)
    for column in features_names:
        if not column in X.columns:
            X[column] = 0
    return X

def get_X(data_manager):
    return data_manager.to_tree()

def undersample(data_manager):
    X, y = get_X_Y(data_manager)
    oversampler = RandomUnderSampler(sampling_strategy=0.2)
    X_resampled, y_resampled = oversampler.fit_resample(X, y)
    return X_resampled, y_resampled

def oversample(data_manager):
    X, y = get_X_Y(data_manager)
    oversampler = RandomOverSampler(sampling_strategy=0.8)
    X_resampled, y_resampled = oversampler.fit_resample(X, y)
    return X_resampled, y_resampled

def smote(data_manager):
    X, y = get_X_Y(data_manager)
    smote_enn = SMOTEENN(sampling_strategy=0.5)
    X_resampled, y_resampled = smote_enn.fit_resample(X, y)
    return X_resampled, y_resampled

def get_X_Y(data_manager):
    X = data_manager.to_tree()
    y = pd.Series(data_manager.labels)
    y = y.loc[X.index]
    if y.isnull().any():
        raise Exception
    return X, y
