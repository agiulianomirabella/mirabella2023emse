import json
import yaml

from ..constants import RESTEST_PATH

from .properties import Properties


def get_spec(properties_path):

    properties = Properties(properties_path)

    oas_path = RESTEST_PATH + properties.get('oas.path')
    conf_path = RESTEST_PATH + properties.get('conf.path')

    with open(conf_path, 'r') as f:
        if conf_path.endswith('json'):
            test_conf = json.load(f)
        elif conf_path.endswith('yaml'):
            test_conf = yaml.safe_load(f)

    endpoint = test_conf['testConfiguration']['operations'][0]['testPath']
    http_method = test_conf['testConfiguration']['operations'][0]['method']

    types = {}
    descriptions = {}
    api_keys = []

    # load the service specification
    with open(oas_path, 'r') as f:
        if oas_path.endswith('json'):
            oas_spec = json.load(f)
        elif oas_path.endswith('yaml'):
            oas_spec = yaml.safe_load(f)
    
    # version 2.0
    if not 'openapi' in oas_spec.keys():
        parameters = oas_spec['paths'][endpoint][http_method]['parameters']
        parameters = __correct_ref(oas_spec, parameters)

        for parameter in parameters:

            # types
            if 'enum' in parameter.keys():
                types.update({parameter['name']: parameter['enum']})
            elif parameter['type']  == 'array':
                types.update({parameter['name']: 'array'})
            elif parameter['type'] in ['boolean']:
                types.update({parameter['name']: 'boolean'})
            elif parameter['type'] in ['string']:
                types.update({parameter['name']: 'text'})
            else:
                types.update({parameter['name']: 'number'})

            # descriptions
            if 'description' in parameter.keys():
                descriptions.update({parameter['name']: __preprocess_description(parameter['description'])})
            else:
                descriptions.update({parameter['name']: ''})

    # version 3.0
    else:
        try:
            parameters = oas_spec['paths'][endpoint][http_method]['parameters']
            parameters = __correct_ref(oas_spec, parameters)

            # types
            for parameter in parameters:
                if 'enum' in parameter['schema'].keys():
                    types.update({parameter['name']: parameter['schema']['enum']})
                # elif 'anyOf' in parameter['schema'].keys():
                #     a = 1
                #     pass
                elif parameter['schema']['type'] in ['bool', 'boolean']:
                    types.update({parameter['name']: 'boolean'})
                elif parameter['schema']['type'] in ['array']:
                    types.update({parameter['name']: 'array'})
                elif parameter['schema']['type'] in ['string']:
                    types.update({parameter['name']: 'text'})
                else:
                    types.update({parameter['name']: 'number'})

            # descriptions
            if 'description' in parameter.keys():
                descriptions.update({parameter['name']: __preprocess_description(parameter['description'])})
            else:
                descriptions.update({parameter['name']: ''})
    
        except Exception as e:

            parameters = oas_spec['paths'][endpoint][http_method]['requestBody']['content']['application/x-www-form-urlencoded']['schema']['properties']

            # types
            for name, values in parameters.items():
                if 'anyOf' in values.keys() or 'enum' in values.keys():
                    types.update({name: 'enum'})
                elif values['type'] in ['bool', 'boolean']:
                    types.update({name: 'enum'})
                elif values['type'] in ['string', 'array']:
                    types.update({name: 'text'})
                else:
                    types.update({name: 'number'})

            # descriptions
            if 'description' in values.keys():
                descriptions.update({name: __preprocess_description(values['description'])})
            else:
                descriptions.update({name: ''})

    if 'YouTube' in properties_path:
        api_keys = ['key']

    spec = {
        'api_keys': api_keys, 
        'types': types, 
        'descriptions': descriptions, 
    }

    return spec

def __correct_ref(spec, parameters):

    # correct '$ref' elements in specification
    for i, parameter in enumerate(parameters):
        if len(parameter.keys()) == 1 and '$ref' in parameter.keys():
            ref_paths = parameter['$ref'].split('/')[1:]
            aux_dict = spec

            for x in ref_paths:
                aux_dict = aux_dict[x]
            parameters[i] = aux_dict

    return parameters

def __preprocess_description(description):
    description = description.replace('\n', ' ')
    return description
