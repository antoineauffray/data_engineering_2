import unittest
import model


class FlaskTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_model_top(self):
        word = 'election'
        df_word_model = model.model(word=word)
        self.assertEqual(len(df_word_model), 20)
    
    def test_model_distance(self):
        word = 'election'
        df_word_model = model.model(word=word)
        self.assertEqual(max(df_word_model.distance) < 0.10, True)

if __name__ == '__main__':
    unittest.main()
