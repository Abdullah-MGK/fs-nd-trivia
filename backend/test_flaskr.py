import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    
    qid = 0
    
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #test_paginate_questions
    
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)
    
    
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['totalQuestions'], 19)
        self.assertEqual(len(data['categories']), 6)
    
    
    def test_get_questions_page_not_exist(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Not Found")
    
    
    def test_search_questions_found(self):
        data = {"searchTerm": "who"}
        res = self.client().post('/questions/search', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 3)
        self.assertEqual(data['totalQuestions'], 3)
        self.assertEqual(len(data['categories']), 2)
    
    
    def test_search_questions_not_found(self):
        data = {"searchTerm": "abcdef"}
        res = self.client().post('/questions/search', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")
    
    
    def test_get_questions_by_category(self):
        res = self.client().get('categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 3)
        self.assertEqual(data['totalQuestions'], 3)
        self.assertEqual(data['currentCategory'], 1)
    
    
    def test_get_questions_by_category_not_exist(self):
        res = self.client().get('categories/100/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")
    
    
    def test_get_next_question(self):
        data = {
            "previous_questions": [],
            "quiz_category": {
                "id": 1,
                "type": "Science"
            }
        }
        res = self.client().post('/quizzes', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['question']), 5)
    
    
    def test_get_next_question_no_more_questions(self):
        data = {
            "previous_questions": ["20","21","22"],
            "quiz_category": {
                "id": 1,
                "type": "Science"
            }
        }
        res = self.client().post('/quizzes', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['question']), 0)
    
    
    def test_add_question(self):
        data = {
            "question": "What is my name?",
            "answer":"Abdullah",
            "category":1,
            "difficulty":1
        }
        res = self.client().post('/questions', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['question']), 5)
        TriviaTestCase.qid = data['question']['id']
    
    
    def test_delete_question(self):
        res = self.client().delete('/questions/{}'.format(TriviaTestCase.qid))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_question'], TriviaTestCase.qid)
    
    
    def test_add_question_category_not_exist(self):
        data = {
            "question": "What is my name?",
            "answer":"Abdullah",
            "category":100,
            "difficulty":1
        }
        res = self.client().post('/questions', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Request")
    
    
    def test_delete_question_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")
    

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TriviaTestCase('test_get_categories'))
    suite.addTest(TriviaTestCase('test_get_questions'))
    suite.addTest(TriviaTestCase('test_get_questions_page_not_exist'))
    suite.addTest(TriviaTestCase('test_search_questions_found'))
    suite.addTest(TriviaTestCase('test_search_questions_not_found'))
    suite.addTest(TriviaTestCase('test_get_questions_by_category'))
    suite.addTest(TriviaTestCase('test_get_questions_by_category_not_exist'))
    suite.addTest(TriviaTestCase('test_get_next_question'))
    suite.addTest(TriviaTestCase('test_get_next_question_no_more_questions'))
    suite.addTest(TriviaTestCase('test_add_question'))
    suite.addTest(TriviaTestCase('test_delete_question'))
    suite.addTest(TriviaTestCase('test_add_question_category_not_exist'))
    suite.addTest(TriviaTestCase('test_delete_question_not_exist'))
    
    return suite

# Make the tests conveniently executable
if __name__ == "__main__":
    #unittest.main()
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())

'''
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
'''  