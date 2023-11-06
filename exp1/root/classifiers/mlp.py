from root import data
from root.classifiers.utils import get_X_Y
import numpy as np

from sklearn.model_selection import train_test_split, StratifiedKFold
from tensorflow.keras import regularizers
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping

class MLP:
    def __init__(self, input_dim):
        self.input_dim = input_dim
        self.optimizer = 'Adam'
        self.batch_size = 8
        self.model = create_model(self.input_dim)
        self.callbacks = [
            EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True),
        ]

    def kfold(self, data_manager):
        accuracies = []

        X, y = get_X_Y(data_manager)
        
        skf = StratifiedKFold(n_splits=10)

        for train_index, test_index in skf.split(X, y):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.15)

            self.model = create_model(self.input_dim)
            self.model.fit(
                x = X_train,
                y = y_train,
                validation_data=(X_valid, y_valid),
                batch_size = self.batch_size,
                epochs = 100,
                callbacks = self.callbacks,
                verbose=0
            )

            scores = self.model.evaluate(X_test, y_test)
            accuracies.append(scores[self.model.metrics_names.index('accuracy')])

        return np.mean(accuracies)



##################### AUXILIARY FUNCTION: ######################

def create_model(input_dim):
    model = Sequential()
    model.add(Dense(32, activation='relu', kernel_regularizer= regularizers.l1_l2(l1=0.0001, l2=0.0001), input_shape=(input_dim, )))
    model.add(Dropout(0.3))
    model.add(Dense(16, activation='relu', kernel_regularizer= regularizers.l1_l2(l1=0.0001, l2=0.0001)))
    model.add(Dropout(0.3))
    model.add(Dense(8,  activation='relu', kernel_regularizer= regularizers.l1_l2(l1=0.0001, l2=0.0001)))
    model.add(Dropout(0.3))
    model.add(Dense(4,  activation='relu', kernel_regularizer= regularizers.l1_l2(l1=0.0001, l2=0.0001)))
    model.add(Dense(2,  activation='relu', kernel_regularizer= regularizers.l1_l2(l1=0.0001, l2=0.0001)))
    model.add(Dense(1,  activation='sigmoid'))
    model.compile(optimizer='Adam', loss='binary_crossentropy', metrics=['accuracy', 'AUC'])
    return model

