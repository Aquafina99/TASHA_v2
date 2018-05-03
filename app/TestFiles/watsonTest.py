import flask
import unittest
from app import app

class WatsonTestCase(unittest.TestCase):
   
    @classmethod
    def setUpClass(cls):
        pass 

    @classmethod
    def tearDownClass(cls):
        pass 

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 

    def tearDown(self):
        pass 

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.post('/tasha/test') 

        # assert the status code of the response
        self.assertEqual(result.status_code, 200) 


    def test_ConceptResult(self):
        result = self.app.get('/tasha/concepts')

        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
