import os
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier

from sklearn.preprocessing import MinMaxScaler

PREDICTOR = RandomForestClassifier(n_estimators=300, criterion='gini')
SCALER = MinMaxScaler()

DEFAULT_RESAMPLING_RATIO = 0.8

RESTEST_PATH = '../RESTest/'

SERVICES = [
    "GitHub", 
    'Amadeus_Hotels', 
    "Stripe_Coupons", 
    "Stripe_Products", 
    "Yelp_Businesses", 
    "YouTube_CommentsAndThreads", 
    "YouTube_Videos", 
    "YouTube_Search", 
]
