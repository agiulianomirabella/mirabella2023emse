import os
from api.root.constants import DEFAULT_RESAMPLING_RATIO, RESTEST_PATH
from api.root.data.dataset import read_dataset
from django.http import JsonResponse

from api.root.data.processing import read_raw

import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-2s %(message)s',
    level=logging.INFO,
    datefmt='[%d/%b/%Y %H:%M:%S]')
logger = logging.getLogger(__name__)

def get_input_parameters(request):

    training_path   = RESTEST_PATH + request.GET['trainingPath']
    properties_path = RESTEST_PATH + request.GET['propertiesPath']

    target_path = None
    if 'targetPath' in request.GET.keys():
        target_path     = RESTEST_PATH + request.GET['targetPath']

    resampling_ratio = DEFAULT_RESAMPLING_RATIO
    if 'resamplingRatio' in request.GET.keys():
        resampling_ratio = float(request.GET['resamplingRatio'])

    logger.info(f'Training path:                {training_path}')
    logger.info(f'Target path:                  {target_path}')
    logger.info(f'Properties path:              {properties_path}')
    logger.info(f'Resampling ratio:             {resampling_ratio}')

    return training_path, target_path, properties_path, resampling_ratio

def get_training_data(training_data_path, spec):
    if not os.path.exists(training_data_path):
        return None, f'No trainingFolder found at {training_data_path}'

    training_data = read_dataset(training_data_path, spec)

    logger.info(f'# valid in training data:     {training_data.n_obt_valid}')
    logger.info(f'# faulty in training data:    {training_data.n_obt_faulty}')

    if training_data.size <= 0:
        return None, f'No valid requests found at {training_data_path}'

    return training_data, 'OK'


def get_target_data(target_path, spec):
    if not os.path.exists(target_path):
        return None, f'No target found at {target_path}'

    target = read_raw(target_path)

    # remove duplicated indices
    target = target[~target.index.duplicated()]

    if target.empty:
        return None, f'No valid requests found at {target_path}'

    logger.info(f'# requests in target:         {len(target.index)}')

    return target, 'OK'

def select_common_features(X_train, X_target):
    common_features = [c for c in X_train.columns if c in X_target.columns]
    X_train  = X_train[common_features]
    X_target = X_target[common_features]

    logger.info(f'# common features:            {len(common_features)}')
    logger.info(f'# X_train columns:            {len(X_train.columns)}')
    logger.info(f'# X_pool columns:             {len(X_target.columns)}')

    return X_train, X_target
