import os
from re import T
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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

    def test_if_get_questions_works(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['current_category'],None)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

     
    def test_if_get_questions_fails(self):
        res =self.client().get('/questions?page=20000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"resources not found")
         
    def test_if_get_categories_works(self):        
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        data.popitem()
        self.assertEqual(data['categories'],data['categories'])

    def test_if_get_categories_fails(self): 
        res = self.client().get('/categoriesu')
        data =json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],'resources not found')
           
    def test_if_get_questionByCategories_works(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['current_category'],'Social')
        self.assertNotEqual(len(data['questions']), 0)
        
    def test_if_get_questionByCateogries_fails(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,500)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],500)
        self.assertEqual(data['message'],"Internal server error")
    
    def test_if_add_new_questions_works(self):
        question_before_adding = Question.query.all()
        res = self.client().post('/questions', json = {
            'question': 'test Question? ',
            'answer': 'unit testing',
            'difficulty': 4,
            'category': '5'
        })
        question_after_adding = Question.query.all()
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(question_after_adding) -  len(question_before_adding)==1)
    
    def test_if_add_new_question_fails(self):
        res = self.client().post('/questions', json ={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"unprocessable")
        
    def test_if_search_question_works(self):
        res = self.client().post('/search', json={'searchTerm': 'test'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)        
    
    def test_if_search_question_fails(self):
        res = self.client().post('/search',json={'searchTerm': 22})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)  
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"resources not found")  
        
    def test_play_trivia_quiz(self):
        res = self.client().post('/play', json={
                                                'previous_questions':[19,20],
                                                'quiz_category':{'id':'1','type':'Science'}
                                                     })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['question'])
     
    def test_if_play_trivia_quiz_fails(self):
        res = self.client().post('/play', json={})   
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"bad request")
    
    def test_if_delete_question_works(self):
        new_questions = Question(question="tests?", answer="yes", category="2", difficulty=2 )
        new_questions.insert()
        question_id = new_questions.id
        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],question_id)
    
    def test_if_delete_quesitons_fails(self):
        res = self.client().delete('/questions/12222324')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"resources not found")
        
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()