import os
import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score

from root.data.processing import raw2preprocessed, read_raw

def read_dataset(path, spec):

    # read test cases and results
    if os.path.exists(path + "/requests.csv") and os.path.exists(path + "/responses.csv"):
        requests  = read_raw(path + "/requests.csv")
        responses = read_raw(path + "/responses.csv")
    else:
        requests_filenames  = [name for name in os.listdir(path) if name.startswith("test-cases")]
        responses_filenames = [name for name in os.listdir(path) if name.startswith("test-results")]
        if len(requests_filenames) > 0 and len(responses_filenames) > 0:
            requests  = pd.concat([read_raw(path + "/" + requests_path) for requests_path in requests_filenames])
            responses = pd.concat([read_raw(path + "/" + responses_path) for responses_path in responses_filenames])
        else:
            raise FileNotFoundError(f'No requests/responses found in {path}.')

    # filter irrelevant status codes
    responses = clean_status_codes(responses)
    requests = requests.loc[responses.index.values]

    return Dataset(requests, responses, spec)

def read_many(path, spec):

    requests = pd.DataFrame()
    responses = pd.DataFrame()

    for dirname in os.listdir(path):
        if os.path.isdir(path+'/'+dirname):
            new_data = read_dataset(path+'/'+dirname, spec)
            requests = pd.concat([requests, new_data.requests])
            responses = pd.concat([responses, new_data.responses])

    return Dataset(requests, responses, spec)

class Dataset:
    def __init__(self, requests, responses, spec):
        self.requests        = requests
        self.responses       = responses
        self.spec            = spec

    def __eq__(self, other):
        if not isinstance(other, Dataset):
            return False
        return self.requests.equals(other.requests) and self.responses.equals(other.responses) and self.spec == other.spec

    ### validities:
    @property
    def exp_validities(self):
        return self.requests['faulty'].apply(lambda x: not x)
    @property
    def obt_validities(self):
        return self.responses['statusCode'].apply(lambda x: is_a_valid_status_code(x))

    ### others: 
    @property
    def size(self):
        return len(self.requests.index)

    def __getattribute__(self, name):

        ### exp/obt/true_valid/faulty_ratio:
        if name.endswith('_valid_ratio') or name.endswith('_faulty_ratio'):

            # if no requests, return 0
            if self.size == 0:
                return 0

            mode, validity = name.split('_')[:-1]

            V = self.__getattribute__('n_'+mode+'_valid')
            F = self.__getattribute__('n_'+mode+'_faulty')

            if validity == 'valid':
                return V/(V+F)
            else:
                return F/(V+F)

        ### exp/obt/true_valid(faulty):
        if name in ["exp_valid", "exp_faulty", "obt_valid", "obt_faulty", "true_valid", "true_faulty"]:
            mode = name.split("_")[0] + "_validities"
            validity = True if name.endswith("valid") else False
            validities = self.__getattribute__(mode)==validity
            return self.requests.loc[validities[validities==True].index]

        ### n_exp/obt/true_valid(faulty):
        if name.startswith("n_"):
            return len(self.__getattribute__(name[2:]))

        ### exp_vs_true_AUC:
        if any([name.startswith(x) for x in ["exp_vs_true", "exp_vs_obt", "obt_vs_true"]]):
            mode1, _, mode2 = name.split("_")[:3]
            validities1 = self.__getattribute__(mode1 + "_validities")
            validities2 = self.__getattribute__(mode2 + "_validities")
            if name.endswith("_AUC"):
                try:
                    return roc_auc_score(validities2, validities1)
                except ValueError as e: # when only one class is present
                    return accuracy_score(validities2, validities1)
            return accuracy_score(validities2, validities1)
        return object.__getattribute__(self, name)

    ### raw2preprocessed interface
    def preprocess_requests(self):
        return raw2preprocessed(self.requests, self.spec)

    def get_oas(self):
        out = self.responses.apply(lambda x: "OAS" in x["failReason"], axis=1).tolist().count(True)
        return int(out)
    
    def get_5XX(self):
        out = self.responses.apply(lambda x: int(x['statusCode']) >= 500 and int(x['statusCode']) < 600, axis=1).tolist().count(True)
        return out
        


# >>> Helpers: >>>
def clean_status_codes(responses):
    responses = responses.drop(responses[responses["statusCode"]=='401'].index) # missing or invalid credentials 
    responses = responses.drop(responses[responses["statusCode"]=='403'].index) # forbidden (insufficient api key permission) 
    responses = responses.drop(responses[responses["statusCode"]=='413'].index) # 
    responses = responses.drop(responses[responses["statusCode"]=='429'].index) # too many requests 
    return responses

def is_a_valid_status_code(x):
    x = int(x)
    is_faulty = x>=400 and x<500
    return not is_faulty