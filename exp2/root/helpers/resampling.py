from imblearn.under_sampling import NearMiss

def resample(X_train, y_train, sampling_ratio):

    n_init_requests = len(X_train.index)

    # compute number of valid and faulty requests
    n_valid  = y_train.tolist().count(True)
    n_faulty = y_train.tolist().count(False)
    n_minority = min(n_valid, n_faulty)
    n_majority = max(n_valid, n_faulty)

    # perform sampling if more than one class present, and the minority ratio is less than the threshold
    if n_minority > 0 and n_minority/n_majority < sampling_ratio:

        # compute the number of neighbors
        n_neighbors=max(1, n_minority)

        # define and execute sampler
        sampler = NearMiss(sampling_strategy=sampling_ratio, n_neighbors=n_neighbors)
        X_train, y_train = sampler.fit_resample(X_train, y_train)
        # print(f'X_train has {y_train.tolist().count(True)} valid and {y_train.tolist().count(False)} faulty requests.')

    n_final_requests = len(X_train.index)

    return X_train, y_train
