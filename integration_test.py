import unittest
from model import app
from flask import Flask

class FlaskTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_model_d2v(self):
        data = {'word_to_analyse':'election', 'model':'d2v'}
        response = self.app.post('http://localhost:5000/', data=data)
        #print(response.data)        
        self.assertEqual(response.status_code,200)
    
    def test_model_w2v(self):
        data = {'word_to_analyse':'election', 'model':'w2v'}
        response = self.app.post('http://localhost:5000/', data=data)
        print(response.data)        
        self.assertEqual(response.status_code,200)
    
if __name__ == '__main__':
    unittest.main()