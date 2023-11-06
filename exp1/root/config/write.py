import os
import yaml
import json

def write_config(api_folder, endpoint, operation):
    if os.path.exists(os.path.join(api_folder, 'swagger.yaml')):
        a_yaml_file = open(os.path.join(api_folder, 'swagger.yaml'))
        spec = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
    else:
        with open(api_folder + 'swagger.json') as json_file:
            spec = json.load(json_file)
    if not 'openapi' in spec.keys():
        parameters = spec['paths'][endpoint][operation]['parameters']
        types = {}
        for parameter in parameters:
            if parameter['type'] in ['enum', 'boolean'] or 'enum' in parameter.keys():
                types.update({parameter['name']: 'enum'})
            elif parameter['type'] in ['string', 'array']:
                types.update({parameter['name']: 'text'})
            else:
                types.update({parameter['name']: 'number'})
            descriptions = {parameter['name']: __description_utils(parameter['description']) if 'description' in parameter.keys() else '' for parameter in parameters}
    else:
        try:
            parameters = spec['paths'][endpoint][operation]['parameters']
            parameters = [p for p in parameters if 'name' in p.keys()]
            types = {}
            for parameter in parameters:
                if 'enum' in parameter['schema'].keys() or parameter['schema']['type'] in ['bool', 'boolean']:
                    types.update({parameter['name']: 'enum'})
                elif parameter['schema']['type'] in ['string', 'array']:
                    types.update({parameter['name']: 'text'})
                else:
                    types.update({parameter['name']: 'number'})
            descriptions = {parameter['name']: __description_utils(parameter['description']) if 'description' in parameter.keys() else '' for parameter in parameters}
        except Exception:
            parameters = spec['paths'][endpoint][operation]['requestBody']['content']['application/x-www-form-urlencoded']['schema']['properties']
            types = {}
            for name, values in parameters.items():
                if 'anyOf' in values.keys() or 'enum' in values.keys():
                    types.update({name: 'enum'})
                elif values['type'] == 'bool':
                    types.update({name: 'enum'})
                elif values['type'] in ['string', 'array']:
                    types.update({name: 'text'})
                else:
                    types.update({name: 'number'})
            descriptions = {name: __description_utils(values['description']) if 'description' in values.keys() else '' for name, values in parameters.items()}

    config = {
        'restest': {
            'properties': '',
            'results': '',
        },
        'types': types,
        'descriptions': descriptions,
        'api_keys': ['key'] if 'YouTube' in api_folder else [],
        'class_weight':'balanced',
        'sample_method':'smote',
    }

    f = open(os.path.join(api_folder, 'config.json'), 'w')
    f.write(json.dumps(config, indent=4))
    f.close()

def __description_utils(description):
    description = description.replace('\n', ' ')
    return description

OAS_KEYS = {
    'Amadeus_Flights':            ['/shopping/flight-offers',      'get'],
    'Amadeus_Hotels':             ['/shopping/hotel-offers',       'get'],
    'GitHub':                     ['/user/repos',                  'get'],
    'Foursquare':                 ['/venues/search',               'get'],
    'LanguageTool':               ['/check',                      'post'],
    'LanguageTool-mod':           ['/check',                      'post'],
    'Stripe_Coupons':             ['/v1/coupons',                 'post'],
    'Stripe_Products':            ['/v1/products',                'post'],
    'Yelp_Businesses':            ['/businesses/search',           'get'],
    'YouTube_CommentsAndThreads': ['/commentThreads',              'get'],
    'YouTube_Videos':             ['/youtube/v3/videos',           'get'],
    'YouTube_Search':             ['/youtube/v3/search',           'get'],
}

API_KEYS = {
    'YouTube_CommentsAndThreads':            ['key'],
    'YouTube_Videos':             ['key'],
    'YouTube_Search':             ['key'],
}
