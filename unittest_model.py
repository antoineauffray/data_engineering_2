import unittest
from similar_tweets import get_similar_tweets
from model import nlp



class FlaskTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_model_top_w2v(self):
        word = 'election'
        model = 'w2v'
        df_word_model = get_similar_tweets(word, model, nlp)
        self.assertEqual(len(df_word_model), 20)
    
    def test_model_top_d2v(self):
        word = 'election'
        model = 'd2v'
        df_word_model = get_similar_tweets(word, model, nlp)
        self.assertEqual(len(df_word_model), 20)
    
    def test_model_distance_w2v(self):
        word = 'election'
        model = 'w2v'
        df_word_model = get_similar_tweets(word, model, nlp)
        self.assertEqual(max(df_word_model.distance) < 0.10, True)

    def test_model_distance_d2v(self):
        word = 'election'
        model = 'd2v'
        df_word_model = get_similar_tweets(word, model, nlp)
        self.assertEqual(max(df_word_model.distance) < 0.35, True)


if __name__ == '__main__':
    unittest.main()
