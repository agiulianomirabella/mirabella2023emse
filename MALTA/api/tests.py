# import json
# from django.test import TestCase, Client
# from django.urls import reverse

# # Create your tests here.

# from api.root.data.dataset import read_dataset
# from api.root.data.processing import read_raw
# from api.root.helpers.spec import get_spec

# class TestApi(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.validity_url = '/validity?trainingPath=target/test-data/GitHub_postman&targetPath=target/test-data/GitHub_postman/validity_pool.csv&resamplingRatio=0.8&propertiesPath=src/test/resources/GitHub/props.properties'
#         self.uncertainty_url = '/uncertainty?trainingPath=target/test-data/GitHub_postman&targetPath=target/test-data/GitHub_postman/uncertainty_pool.csv&nTests=5&resamplingRatio=0.8&propertiesPath=src/test/resources/GitHub/props.properties'
#         self.train_url = '/train?trainingPath=target/test-data/GitHub_postman&resamplingRatio=0.8&propertiesPath=src/test/resources/GitHub/props.properties'
#         self.spec = get_spec('/Users/giulianomirabella/Desktop/RESTest/src/test/resources/GitHub/props.properties')
#         self.base_dir = '/Users/giulianomirabella/Desktop/RESTest/target/test-data'

#     def test_validity(self):

#         # Get the initial training dataset
#         init_training_data = read_dataset(self.base_dir + '/GitHub_postman/', self.spec)

#         # Get the initial target, then invoke the API
#         init_target = read_raw(self.base_dir + '/GitHub_postman/validity_pool.csv')
#         response = self.client.get(self.validity_url)

#         # Check status code is OK
#         self.assertEquals(response.status_code, 200)

#         # Get the final training dataset and assert it is equal to the initial one
#         final_training_data = read_dataset(self.base_dir + '/GitHub_postman/', self.spec )
#         self.assertEquals(init_training_data, final_training_data)

#         # Get the final target
#         final_target = read_raw(self.base_dir + '/GitHub_postman/validity_pool.csv')

#         # Check modified columns only contain: true, false or null
#         self.assertTrue(all([v in ['true', 'false'] for v in set(final_target.faulty)]))
#         self.assertTrue(all([v in ['true', 'false'] for v in set(final_target.fulfillsDependencies)]))
#         self.assertTrue(all([v in ['inter_parameter_dependency', 'null'] for v in set(final_target.faultyReason)]))

#         # Check that the rest of data has not changed
#         init_target  = init_target.drop(columns=['faulty', 'faultyReason', 'fulfillsDependencies'])
#         final_target = final_target.drop(columns=['faulty', 'faultyReason', 'fulfillsDependencies'])
#         self.assertTrue(all([i in init_target.index for i in final_target.index]))

#     def test_uncertainty(self):

#         # Get the initial training dataset
#         init_training_data = read_dataset(self.base_dir + '/GitHub_postman/', self.spec)

#         # Get the initial target, then invoke the API
#         init_target = read_raw(self.base_dir + '/GitHub_postman/uncertainty_pool.csv')
#         response = self.client.get(self.uncertainty_url)

#         # Check status code is OK
#         self.assertEquals(response.status_code, 200)

#         # Get the final training dataset and assert it is equal to the initial one
#         final_training_data = read_dataset(self.base_dir + '/GitHub_postman/', self.spec )
#         self.assertEquals(init_training_data, final_training_data)

#         # Get the final target
#         final_target = read_raw(self.base_dir + '/GitHub_postman/uncertainty_pool.csv')

#         # Check modified columns only contain: true, false or null
#         self.assertTrue(all([v in ['true', 'false'] for v in set(final_target.faulty)]))
#         self.assertTrue(all([v in ['true', 'false'] for v in set(final_target.fulfillsDependencies)]))
#         self.assertTrue(all([v in ['inter_parameter_dependency', 'null'] for v in set(final_target.faultyReason)]))

#         # Check that the rest of data has not changed
#         init_target  = init_target.drop(columns=['faulty', 'faultyReason', 'fulfillsDependencies'])
#         final_target = final_target.drop(columns=['faulty', 'faultyReason', 'fulfillsDependencies'])
#         self.assertTrue(all([i in init_target.index for i in final_target.index]))

#     def test_train(self):

#         # Get the initial training dataset
#         init_training_data = read_dataset(self.base_dir + '/GitHub_postman/', self.spec)

#         # Invoke the API
#         response = self.client.get(self.train_url)

#         # Check status code is OK
#         self.assertEquals(response.status_code, 200)

#         # Get the final training dataset and assert it is equal to the initial one
#         final_training_data = read_dataset(self.base_dir + '/GitHub_postman/', self.spec )
#         self.assertEquals(init_training_data, final_training_data)

#         # Check score >= 0.9
#         self.assertTrue(response.json()['score'] >= 0.9)



