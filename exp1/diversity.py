from root.classifiers.utils import get_X_Y
from root.data.utils import SERVICES
import numpy as np
import pandas as pd

from root.data.manager import DataManager

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

for service in SERVICES:
    data_manager = DataManager('data/' + service)
    
    X, y = get_X_Y(data_manager)

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print(service)
    print(X_scaled.shape)

    # Perform PCA
    pca = PCA()
    X_pca = pca.fit_transform(X_scaled)

    # Calculate the explained variance ratio
    explained_variance_ratio = pca.explained_variance_ratio_

    # Plot the explained variance ratio
    plt.plot(np.cumsum(explained_variance_ratio))
    plt.xlabel('Number of Principal Components')
    plt.ylabel('Cumulative Explained Variance')
    plt.title('Explained Variance Ratio')
    plt.savefig(f'diversity-results/{service}.png')
    plt.close()

