import json
import os

def get_config(file_name):
   f = open(os.path.join(file_name, 'config.json'), 'r')
   config = json.load(f)
   f.close()
   return config

def pretty(d):
   print(json.dumps(d, indent=4))