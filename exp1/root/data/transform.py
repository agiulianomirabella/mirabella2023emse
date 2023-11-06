import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from root.data.utils import key_value_preprocessing, is_api_key
from root.data.encoding import encode_enum, encode_number, encode_text, normalize, onehot


'''
* raw form: RESTest target csv format
* normal form:
    - column --> value
* complete form:
    - texts presence boolean encoding
    - numbers presence boolean encoding
    - fill empty values in numbers with 0s
    - fill empty values in enums with NONEs
* tree form:
    - (complete form)
    - one-hot-encodes enums
    - max-min-scale numbers
'''

def raw2complete(raw, types, api_keys):
    return __normal2complete(__raw2normal(raw, types, api_keys), types)

def __normal2complete(normal, types):
    for column in types.keys(): # adjusts types.keys and normal.columns for the complete df to be always of the same number of columns:
        if not column in normal.columns:
            normal[column] = np.nan

    if not list(normal.columns).sort() == list(types.keys()).sort():
        raise Exception('ERROR: normal columns and types keys are not equal.')

    for column, type_value in types.items():
        if type_value == 'text':
            normal = encode_text(normal, column)
        elif type_value == 'number':
            normal = encode_number(normal, column)
        else:
            normal = encode_enum(normal, column)
    complete = normal
    return complete

def __raw2normal(raw, types, api_keys):
    target_columns= [p for p in ['queryParameters', 'formParameters', 'bodyParameter', 'pathParameters'] if not raw[p].empty]
    raw = raw[target_columns]
    raw = raw.fillna('')

    requests = []

    for testId, row in raw.iterrows():
        new_request = {}
        for column in target_columns:
            parameters = row[column].split(';')[:-1]

            for parameter in parameters:
                key, value = parameter.split('=')
                if not is_api_key(key, api_keys):
                    key, value = key_value_preprocessing(key, value, types)
                    new_request.update({
                        key: value
                    })

        new_request.update({
            'testId': testId
        })
        
        requests.append(new_request)

    normal = pd.DataFrame(requests)
    if normal.empty:
        return pd.DataFrame()
    normal = normal.set_index('testId')
    return normal

def complete2tree(complete):
    complete = onehot(complete)
    tree = normalize(complete)
    return tree
