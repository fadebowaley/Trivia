import os
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
        self.database_name = "Trivia-test-app"
        self.db_user = "postgres"
        self.db_password = "root"
        self.db_local_host = "localhost:5432"
        self.database_path = f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_local_host}/{self.database_name}"


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

    #Test 1 -GET all question including pagination (every 10 questions)
    def test_if_get_questions_works(self):
        res = self.client().get('/api/v1.0/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['current_category'] )
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    # Test 2: GET 404 for retrieving questions beyond valid page
    def test_if_get_questions_fails(self):
        res = self.client().get('/api/v1.0/questions?page=20000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"resources not found")

    # Test 3: GET all available categories
    def test_if_get_categories_works(self):
        res = self.client().get('/api/v1.0/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        data.popitem()
        self.assertEqual(data['categories'],data['categories'])


    # Test 4. Get category that does not exist, return 404
    def test_if_get_categories_fails(self): 
        res = self.client().get('/api/v1.0/categoriesu')
        data =json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],'resources not found')

    #Test 5. Get a Question Id by its Category       
    def test_if_get_questionByCategories_works(self):
        res = self.client().get('/api/v1.0/categories/4/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['current_category'],'Science')
        self.assertNotEqual(len(data['questions']), 0)

    # Test 6. Get questions that does not exists return Error 500   
    def test_if_get_questionByCateogries_fails(self):
        res = self.client().get('/api/v1.0/categories/1000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,500)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],500)
        self.assertEqual(data['message'],"Internal server error")
    
    #Test 7. Add/Create a new question
    def test_if_add_new_questions_works(self):
        question_before_adding = Question.query.all()
        res = self.client().post('/api/v1.0/questions', json={
            'question': 'Why Unit Testing? ',
            'answer': 'unit testing',
            'difficulty': 4,
            'category': '5'
        })
        question_after_adding = Question.query.all()
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(question_after_adding) -  len(question_before_adding)==1)
    
    

    # Test 8 -  Question creation is not allowed on empty body, return 422 ERROR
    def test_if_add_new_question_fails(self):
        res = self.client().post('/api/v1.0/questions', json ={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"unprocessable")

    

    #Test 9. Search on any available questions in the Database    
    def test_if_search_question_works(self):
        res = self.client().post('/api/v1.0/search', json={'searchTerm': 'Unit'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)

    #Test 10. Search a question that does not exists, return 404
    def test_if_search_question_fails(self):
        res = self.client().post('/api/v1.0/search', json={'searchTerm': 21052024})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)  
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], "resources not found")

    #Test 10. Play Trivia Quiz sucessfully     
    def test_play_trivia_quiz_works(self):
        res = self.client().post('/api/v1.0/play', json={
                                                'previous_questions':[2,5],
                                                'quiz_category':{'id':'1','type':'Science'}
                                                     })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['question'])

     
    # Test if Trivia Quizzes Fails 
    def test_if_play_trivia_quiz_fails(self):
        res = self.client().post('/api/v1.0/play', json={})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], "unprocessable")
    
    def test_if_delete_question_works(self):
        new_questions = Question(question="tests?", answer="yes", category="2", difficulty=2 )
        new_questions.insert()
        question_id = new_questions.id
        res = self.client().delete('/api/v1.0/questions/{}'.format(question_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],question_id)
    
    def test_if_delete_quesitons_fails(self):
        res = self.client().delete('/api/v1.0/questions/12222324')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],"resources not found")
        
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()