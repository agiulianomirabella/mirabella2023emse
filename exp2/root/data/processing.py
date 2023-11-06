import itertools
import pandas as pd
from urllib.parse import unquote

from root.helpers.spec import get_spec
from root.data.encodings import encode_boolean, encode_datetime, encode_enum, encode_number, encode_text, is_boolean_serie

def raw2preprocessed(raw, spec):

    # get service api keys and parameters types
    api_keys = spec['api_keys']
    types = spec['types']

    # subselect relevant columns
    raw = raw[['queryParameters', 'formParameters', 'bodyParameter', 'pathParameters']]

    # drop columns where all values are empty
    raw = raw.dropna(how='all', axis=1)
    if raw.empty:
        return pd.DataFrame()

    # fill non-empty columns
    raw = raw.fillna('')

    # define a new 'pre_encoding_data' dataset
    df_non_dummies = pd.DataFrame(columns=types.keys(), index=raw.index)

    for testId, row in raw.iterrows():

        for column in raw.columns:
            key_value_pairs = row[column].split(';')[:-1]

            for key_value in key_value_pairs:
                key, value = key_value.split('=')

                # add key-value to the new row (if not an api key)
                if not key in api_keys:

                    # add the new row to the pre_encoding_data dataset
                    df_non_dummies.loc[testId, key] = value

    # change packagedimensions%5B%5D to packagedimensions[]
    df_non_dummies = df_non_dummies.rename(columns={x: unquote(x) for x in df_non_dummies.columns})

    dummies_columns = []
    for k, v in types.items():
        if isinstance(v, list):
            dummies_columns.append(f"{k}")
            for value in v:
                dummies_columns.append(f"{k}=='{value}'")
        elif v=='boolean':
            dummies_columns.append(f"{k}")
            dummies_columns.append(f"{k}=='true'")
            dummies_columns.append(f"{k}=='false'")
        elif v=='number':
            dummies_columns.append(f'{k}')
            dummies_columns.append(f'{k}_value')
        elif v=='text':
            dummies_columns.append(f'{k}')

    # Create example dataframes
    df_dummies = pd.DataFrame(columns=dummies_columns, index=raw.index)

    # Fill in the dummies
    for test_id, row in df_non_dummies.iterrows():
        for column, val in row.iteritems():
            if isinstance(types[column], list):
                if str(val) != 'nan':
                    df_dummies.loc[test_id, f"{column}"] = 1
                    df_dummies.loc[test_id, f"{column}=='{val}'"] = 1
            elif types[column]=='array':
                if str(val) != 'nan':
                    df_dummies.loc[test_id, f"{column}"] = 1
                    df_dummies.loc[test_id, f"{column}=='{val}'"] = 1
            elif types[column]=='boolean':
                if str(val) != 'nan':
                    df_dummies.loc[test_id, f"{column}"] = 1
                    df_dummies.loc[test_id, f"{column}=='{val}'"] = 1
            elif types[column]=='number':
                if str(val) != 'nan':
                    df_dummies.loc[test_id, f"{column}"] = 1
                    df_dummies.loc[test_id, f"{column}_value"] = val
            elif types[column]=='text':
                if str(val) != 'nan':
                    df_dummies.loc[test_id, f"{column}"] = 1

    return df_dummies.fillna(0).sort_index(axis=1)

def read_raw(raw_path):

    # Correct commas
    with open(raw_path, "r") as f:
        lines = f.readlines()
    lines = [l.replace(", but", "but") for l in lines]
    with open(raw_path, "w") as f:
        f.writelines(lines)

    # Read the csv
    raw = pd.read_csv(raw_path, dtype=str)

    # Set the index
    if "testCaseId" in raw.columns:
        raw = raw.set_index("testCaseId")
    else:
        raw = raw.set_index("testResultId")
    return raw

def label_requests(raw, predictions):

    # label 'faulty' column
    raw.loc[predictions[predictions==False].index, 'faulty']='true'
    raw.loc[predictions[predictions==True].index,  'faulty']='false'

    # label 'faultyReason' column
    raw.loc[predictions[predictions==False].index, 'faultyReason']='inter_parameter_dependency'
    # raw.loc[predictions[predictions==True].index,  'faultyReason']='null'

    # label 'fulfillsDependencies' column
    raw.loc[predictions[predictions==False].index, 'fulfillsDependencies']='false'
    raw.loc[predictions[predictions==True].index,  'fulfillsDependencies']='true'

    return raw
