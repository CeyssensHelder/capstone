import os
import unittest
import requests
import re
from ast import literal_eval
import numpy as np

port = 5000

try:
    requests.post('http://127.0.0.1:{}/predict'.format(port))
    server_available = True
except:
    server_available = False
    
## test class for the main window function
class ApiTest(unittest.TestCase):
    """
    test the essential functionality
    """

    @unittest.skipUnless(server_available,"local server is not running")
    def test_01_train(self):
        """
        test the train functionality
        """
      
        request_json = {'mode':'test'}
        r = requests.post('http://127.0.0.1:{}/train'.format(port),json=request_json)
        train_complete = re.sub("\W+","",r.text)
        self.assertEqual(train_complete, 'messageTrainingsuccessful')
    
    @unittest.skipUnless(server_available,"local server is not running")
    def test_02_predict_empty(self):
        """
        ensure appropriate failure types
        """
    
        ## provide no data at all 
        r = requests.post('http://127.0.0.1:{}/predict'.format(port), json={}, headers={'Content-Type': 'application/json'})
        self.assertEqual(re.sub('\n|"','',r.text), '{message:No request data found}')

        ## provide improperly formatted data
        r = requests.post('http://127.0.0.1:{}/predict'.format(port),json={"key":"value"}, headers={'Content-Type': 'application/json'})     
        self.assertEqual(re.sub('\n|"','',r.text), '{message:No query data found}')
    
    @unittest.skipUnless(server_available,"local server is not running")
    def test_03_predict(self):
        """
        test the predict functionality
        """

        # the query dat must be: country, year, month, day

        query_data = {'country': 'netherlands',
                        'year': '2018',
                        'month': '1',
                        'day': '5'
        }

        query_type = 'dict'
        request_json = {'query':query_data,'type':query_type,'mode':'test'}

        r = requests.post('http://127.0.0.1:{}/predict'.format(port),json=request_json)

        self.assertNotEqual(re.sub('\n|"','',r.text), '{message:No query data found}')

    @unittest.skipUnless(server_available,"local server is not running")
    def test_04_logs(self):
        """
        test the log functionality
        """

        file_name = 'train-test.log'
        request_json = {'file':'train-test.log'}
        r = requests.get('http://127.0.0.1:{}/logs/{}'.format(port,file_name))

        with open(file_name, 'wb') as f:
            f.write(r.content)
        
        self.assertTrue(os.path.exists(file_name))

        if os.path.exists(file_name):
            os.remove(file_name)

        
### Run the tests
if __name__ == '__main__':
    unittest.main()
