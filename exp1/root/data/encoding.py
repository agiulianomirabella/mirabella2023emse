import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from pandas.api.types import is_numeric_dtype

N_BINS = 5

def encode_enum(data, column, presences=True):
    if presences:
        data[column + '_presence'] = data[column].notna().astype(bool)
        data[column + '_value']    = __fill_enum(data[column])
        data = data.drop(column, axis=1)
    else:
        data[column] = __fill_enum(data[column])
    return data

def encode_text(data, column):
    if column in data.columns:
        data[column + '_presence'] = data[column].notna().astype(bool)
        data = data.drop(column, axis=1)
    else:
        data[column + '_presence'] = False
    return data

def encode_number(data, column):
    # Stores the numerical value in a new column named oldcolumn_value; then encodes numerical columns as present or not
    if column in data.columns:
        data[column + '_value']    = pd.to_numeric(data[column].fillna(0))
        data[column + '_presence'] = data[column].notna().astype(bool)
        data = data.drop(column, axis=1)
    else:
        data[column + '_value']    = 0
        data[column + '_presence'] = False
    return data

def onehot(data):
    # One-hot encodes enum columns
    for column in data.columns:
        if data.dtypes[column] == np.dtype('O'):
            data[column] = data[column].astype('category')
    return pd.get_dummies(data, prefix_sep='==', dtype=bool)

def normalize(data):
    # Max-min scales number columns
    number_columns = []
    for column in data.columns:
        if is_numeric_dtype(data[column]):
            number_columns.append(column)
            data[column] = pd.cut(data[column], N_BINS, labels=False)
    data[number_columns] = MinMaxScaler().fit_transform(data[number_columns])
    return data

def __fill_enum(serie):
    dummy_value = 'NONE'
    serie = serie.fillna(dummy_value)
    serie = serie.astype('category')
    return serie






# def bool2int(data, valid=False):
#     columns = list(data.select_dtypes(include = ['bool']).columns)
#     if not valid:
#         columns.remove('valid')
#     for column in columns:
#         data[column] = data[column].astype(int)
#     return data


# def label(data):
#     # Label encodes enum columns
#     le = LabelEncoder()
#     columns = list(data.select_dtypes(include = ['category']).columns)
#     # columns = list(data.select_dtypes(include = ['category', 'object']).columns)
#     for column in columns:
#         data[column] = le.fit_transform(data[column])
#     return data




# Fill empty values in a categorical column with dummy_value. Default 'NONE'
# if all([np.isnan(x) for x in serie.values]):
#     return 
# if not 'NONE' in serie.values:
# dummy_value = 'NONE'
# else:
#     raise Exception('the value "NONE" is in the dataframe, enum values could not be filled')
#     # i = 0
#     # while any(serie.isin([dummy_value]).any()):
#     #     i = i+1
#     #     dummy_value = 'NONE' + str(i)
