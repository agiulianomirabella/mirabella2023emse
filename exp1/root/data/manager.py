import os
import json
import pandas as pd
from root.config.read import get_config
from root.data.transform import complete2tree, raw2complete


class DataManager:
    def __init__(self, file_name):
        raw = pd.read_csv(os.path.join(file_name, 'raw.csv'), index_col=0)
        # drop duplicates:
        raw      = raw.loc[raw.index.drop_duplicates(keep ='first')] # pylint: disable=no-member
        raw      = raw.drop_duplicates()

        # set attributes:
        self.raw = raw
        self.config = get_config(file_name)
        self.complete = raw2complete(self.raw, self.config['types'], self.config['api_keys'])
        self.labels = ~self.raw['faulty']

    def to_tree(self):
        return complete2tree(self.complete.drop_duplicates())

    def sample(self, frac):
        self.raw = self.raw.sample(frac = frac)
        self.complete = raw2complete(self.raw, self.config['types'], self.config['api_keys'])
        self.labels = ~self.raw['faulty']

