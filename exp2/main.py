import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score, cohen_kappa_score
from root.data.dataset import read_dataset
from root.constants import SERVICES, PREDICTOR, RESTEST_PATH, SCALER
from root.helpers.spec import get_spec
from root.helpers.resampling import resample
from root.data.utils import select_common_features

out = pd.DataFrame(columns=['service', 'tech', 'dirname', 'accuracy', 'AUC', 'kappa'])

for service in SERVICES:

    properties_path = RESTEST_PATH + f'src/test/resources/{service}/props.properties'
    spec = get_spec(properties_path)

    for i in range(3):

        for tech in ['active', 'random']:

            training_data = read_dataset(f'data/train/{service}/{tech}/{service}_{tech}_{i}', spec)
            test_data = read_dataset(f'data/test/{service}/{service}_test_{i}', spec)

            X_train = training_data.preprocess_requests()
            y_train = training_data.obt_validities
            X_test  = test_data.preprocess_requests()
            y_test  = test_data.obt_validities

            X_train, y_train = resample(X_train, y_train, 1)

            X_train, X_test = select_common_features(X_train, X_test)

            scaler  = SCALER
            X_train = scaler.fit_transform(X_train)
            X_test  = scaler.transform(X_test)

            predictor = PREDICTOR
            predictor.fit(X_train, y_train)

            y_pred = predictor.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            auc = roc_auc_score(y_test, y_pred)
            kappa = cohen_kappa_score(y_test, y_pred)

            out = out.append(pd.Series({
                'service': service,
                'tech': tech,
                'dirname': f'{service}_{tech}_{i}',
                'accuracy': accuracy, 
                'AUC': auc, 
                'kappa': kappa, 
            }), ignore_index=True)

out = out.groupby(['service', 'tech']).mean().reset_index()
out.to_csv('results.csv', index=False)

out = pd.pivot_table(out, index='service', columns='tech', values=['accuracy', 'kappa'])
out.columns = [f'{col}_{tech}' for col, tech in out.columns]
out = out[['accuracy_random', 'accuracy_active', 'kappa_random', 'kappa_active']]
out.loc['Mean'] = out.mean()

print(out)
