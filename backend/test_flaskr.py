import os,sys
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
        self.app=create_app(db_path=self.database_path)
        self.client=self.app.test_client()
        

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        resp=self.client.get('/api/categories/').json
        self.assertTrue(resp['success'])
        self.assertEqual(len(resp['categories']),6)

    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()