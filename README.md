## Full Stack Trivia - Project 2 

### Backend
These are the major files in the backend:
1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*
>View the [README within ./backend for more details.](./frontend/README.md)

### Frontend
1. *./frontend/src/components/QuestionView.js*
2. *./frontend/src/components/FormView.js*
3. *./frontend/src/components/QuizView.js*
>View the [README within ./frontend for more details.](./frontend/README.md)

##  To start the Application - BACKEND
1. cd into backend
2. create virtual environment i.e python3 -m venv env
3. pip Install the requirements.txt example -  pip install -r requirments
4. set the FLASK_APP i.e export FLASK_APP=flaskr/__init__.py
5. set the Enviroment to 'Development i.e 'export FLASK_ENV=development
6. Run the app - flask run

##  To start the Application - FrontEnd
1. cd into frontend
2. cmd npm install
3. To run frontend application npm start


## The Endpoints Documentation

## 1. GET '/api/v1.0/categories'

Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
Request Arguments: None
Returns: An object with a single key, categories, that contains an object of id: category_string key: value pairs.
{
   "categories" : {
      "1" : "Academy",
      "2" : "Social",
      "3" : "Entertainment",
      "4" : "Science"
   },
   "success" : true
}
## 1. GET '/api/v1.0/questions'

Fetches a dictionary of questions in which the keys are the ids and the value is the corresponding string of the category
Request Arguments: None
Returns: An object with a single key, categories, that contains an object of id: category_string key: value pairs.
{
   "categories" : {
      "1" : "Academy",
      "2" : "Social",
      "3" : "Entertainment",
      "4" : "Science"
   },
   "success" : true
}



1. Endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.

2. Endpoint to handle GET requests for all available categories.

3. Endpoint to DELETE question using a question ID.

4. Endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.

5. [ ] Create a POST endpoint to get questions based on category.

6. [ ] Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.

7. [ ] Create a POST endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random question within the given category if provided, and that is not one of the previous questions.
