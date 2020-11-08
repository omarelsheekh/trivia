import os
import sys
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_path = "postgres:///{}".format(self.database_name)
        self.app = create_app(db_path=self.database_path)
        self.client = self.app.test_client()
        self.test_question = Question('test question', 'test answer', 1, 5)

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        resp = self.client.get('/api/categories/').json
        self.assertTrue(resp['success'])
        self.assertEqual(len(resp['categories']), 6)

    def test_get_all_questions(self):
        resp = self.client.get('/api/questions/').json
        self.assertTrue(resp['success'])

    def test_delete_question(self):
        self.test_question.insert()
        resp = self.client.delete(
            '/api/questions/{}'.format(self.test_question.id)).json
        self.assertTrue(resp['success'])

    def test_post_question(self):
        resp = self.client.post(
            '/api/questions/',
            json={
                'question': 'POST_QUSTION',
                'answer': '',
                'category': 1,
                'difficulty': 1}).json
        self.assertTrue(resp['success'])

    def search_question(self):
        self.test_question.insert()
        resp = self.client.post(
            '/api/search/questions',
            json={
                'searchTerm': 'test'}).json
        self.assertTrue(resp['success'])
        self.assertTrue(len(resp['questions']) > 0)

    def test_get_questions_by_category(self):
        resp = self.client.get('/api/categories/1/questions/').json
        self.assertTrue(resp['success'])
        self.assertTrue(len(resp['questions']) > 0)

    def test_play(self):
        resp = self.client.post('/api/quizzes/', json={
            'quiz_category': {'id': 1},
            'previous_questions': [24, 25, 26, 27, 28]
        }).json
        self.assertTrue(resp['success'])
        self.assertFalse(resp['question']['id'] in [24, 25, 26, 27, 28])

    def test_page_not_found(self):
        resp = self.client.get('/api/questions/?page=1000').json
        self.assertFalse(resp['success'])
        self.assertEqual(resp['message'], 'Not Found')

    def test_category_not_found(self):
        resp = self.client.get('/api/categories/10000000/questions/').json
        self.assertFalse(resp['success'])
        self.assertEqual(resp['message'], 'Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
