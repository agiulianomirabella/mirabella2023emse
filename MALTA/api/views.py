from email import message
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import numpy as np
import os

from api.root.data.utils import get_input_parameters, get_target_data, get_training_data, select_common_features, select_most_diverse_rows, select_most_diverse_rows2
from api.root.helpers.spec import get_spec
from api.root.data.dataset import read_dataset, read_raw, raw2preprocessed
from api.root.constants import SCALER, PREDICTOR
from api.root.helpers.resampling import resample
from api.root.data.processing import label_requests
from api.root.helpers.scores import compute_scores

import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-2s %(message)s',
    level=logging.INFO,
    datefmt='[%d/%b/%Y %H:%M:%S]')
logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
    return render(request, "api/index.html")


def validity(request):
    '''
    Input:
        - trainingPath
        - targetPath
        - resamplingRatio
        - propertiesPath
    '''

    print('\n\n')

    # Check http method is GET
    if request.method != 'GET':
        return JsonResponse({"error": "GET request required."}, status=400)

    # Get input parameters:
    training_path, target_path, properties_path, resampling_ratio = get_input_parameters(request)

    # Get spec (types, api_keys, descriptions)
    spec = get_spec(properties_path)

    # Get training data
    train_data, message = get_training_data(training_path, spec)
    if message != 'OK':
        return JsonResponse({'message': message})

    # Get target data
    target_data, message = get_target_data(target_path, spec)
    if message != 'OK':
        return JsonResponse({'message': message}, status=400)

    # Process train data
    X_train = train_data.preprocess_requests()
    y_train = train_data.obt_validities

    # Process pool data
    X_target = raw2preprocessed(target_data, spec)

    # Resample and compute certainty threshold
    X_train, y_train = resample(X_train, y_train, resampling_ratio)

    # Subselect the common features
    X_train, X_target = select_common_features(X_train, X_target)

    # Scale data
    scaler  = SCALER
    X_train = scaler.fit_transform(X_train)
    X_target  = scaler.transform(X_target)

    # Define and fit the predictor
    predictor = PREDICTOR
    predictor.fit(X_train, y_train)

    # Label the pool with predictions
    predictions = pd.Series(predictor.predict(X_target), index=target_data.index)
    target_data = label_requests(target_data, predictions)

    # Compute and sort predicted probabilities
    probabilities = pd.Series(np.max(predictor.predict_proba(X_target), axis=1), index=target_data.index).sort_values(ascending=False)

    # Subselect and sort pool rows
    target_data = target_data.loc[probabilities.index]

    # Write query requests
    target_data.to_csv(target_path)

    n_valid  = len(target_data[target_data['faulty']=='false'].index)
    n_faulty = len(target_data[target_data['faulty']=='true'].index)

    logger.info(f'         Valid request found: {n_valid}')
    logger.info(f'        Faulty request found: {n_faulty}')

    return JsonResponse({'message': f'Validity prediction made upon {target_path}'}, status=200)


def uncertainty(request):
    '''
        Input:
        - trainingPath
        - targetPath
        - resamplingRatio
        - propertiesPath
    '''

    print('\n\n')

    if request.method != 'GET':
        return JsonResponse({"error": "GET request required."}, status=400)
    
    # Get input parameters:    
    training_path, target_path, properties_path, resampling_ratio = get_input_parameters(request)

    # Get spec {types, api_keys, descriptions}
    spec = get_spec(properties_path)

    # Get target data
    target_data, message = get_target_data(target_path, spec)
    if message != 'OK':
        return JsonResponse({'message': message}, status=400)

    requests_filenames  = [name for name in os.listdir(training_path) if name.startswith("test-cases")]
    responses_filenames = [name for name in os.listdir(training_path) if name.startswith("test-results")]

    if len(requests_filenames) == 0 or len(responses_filenames) == 0:
        query = target_data
    else:

        # Get training data
        train_data, message = get_training_data(training_path, spec)
        if message != 'OK':
            return JsonResponse({'message': message})

        # Preprocess train data
        y_train = train_data.obt_validities

        # Preprocess train data
        X_train = train_data.preprocess_requests()

        # Transform train/pool data to tree form
        X_target = raw2preprocessed(target_data, spec)

        if len(set(y_train)) < 2:
            query = target_data
        else:
            
            # Subselect the common features
            X_train, X_target = select_common_features(X_train, X_target)

            # Scale data
            scaler   = SCALER
            X_train  = scaler.fit_transform(X_train)
            X_target = scaler.transform(X_target)

            # Define and fit the predictor
            predictor = PREDICTOR
            predictor.fit(X_train, y_train)

            # Label the pool with predictions
            predictions = pd.Series(predictor.predict(X_target), index=target_data.index)
            target_data = label_requests(target_data, predictions)

            # Compute and sort predicted probabilities
            probabilities = pd.Series(np.max(predictor.predict_proba(X_target), axis=1), index=target_data.index).sort_values(ascending=True)

            # Query first n_tests requests
            query = target_data.loc[probabilities.index]

    query.to_csv(target_path)

    return JsonResponse({'message': f'Uncertainty prediction made upon {target_path}'}, status=200)


def train(request):
    '''
        Input:
        - trainingPath
        - resamplingRatio
        - propertiesPath
    '''

    print('\n\n')

    # Check http method is GET
    if request.method != 'GET':
        return JsonResponse({"error": "GET request required."}, status=400)
    
    # Get input parameters:
    training_path, target_path, properties_path, resampling_ratio = get_input_parameters(request)

    # Get spec (types, api_keys, descriptions)
    spec = get_spec(properties_path)

    # Get training data
    train_data, message = get_training_data(training_path, spec)
    if message != 'OK':
        return JsonResponse({'message': message})

    # If too few requests, return 0
    if train_data.size < 20:
        return JsonResponse({'score': float(0)}, status=200)
    else:
        # preprocess train data
        X_train = train_data.preprocess_requests()
        y_train = train_data.obt_validities

        # resample and compute certainty threshold
        X_train, y_train = resample(X_train, y_train, resampling_ratio)

        # scale data
        scaler  = SCALER
        X_train = scaler.fit_transform(X_train)

        # define and fit the predictor
        predictor = PREDICTOR
        predictor.fit(X_train, y_train)

        # kfold cross validation of the predictor:
        accuracy, roc_auc = compute_scores(predictor, X_train, y_train)    
        score = min(accuracy, roc_auc)

        # print score to be parsed by RESTest
        return JsonResponse({'score': float(score)}, status=200)

