## Full Stack Trivia - Project 2 [https://github.com/fadebowaley]

[API ENDPOINTS DOCUMENTATIONS]

## Endpoints - fixed as commented on review 
GET '/api/v1.0/categories'
GET '/api/v1.0/questions'
GET '/api/v1.0/categories/<int:id>/questions'
POST '/api/v1.0/questions'
POST '/api/v1.0/search'
POST '/api/v1.0/play'
DELETE '/api/v1.0/questions/<int:id>'




## 1. GET '/api/v1.0/categories'

Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
Request Arguments: None
Returns: An object with a single key, categories, that contains an object of id: category_string key: value pairs.

Example below :
{
"categories" : {
"1" : "Academy",
"2" : "Social",
"3" : "Entertainment",
"4" : "Science"
},
"success" : true
}

## 2. GET '/api/v1.0/questions'

Fetches a dictionary of questions, answers, category and difficulty in which the keys are the ids and the value is the corresponding strings
Request Arguments: None
Returns: dictionary of objects that contains key: value pairs with total_questions and values

Example below:
{
"answer" : "nothing else",
"category" : "2",
"difficulty" : 2,
"id" : 10,
"question" : "Who owns Google?"
}
],
"success" : true,
"total_questions" : 1
}

## 3. DELETE /api/v1.0/questions/<int:id>'

Handles deletion of questions using a question ID
returns {"deleted":8,"success":true} questions' id deleted and success as True if deletion successfully occur.

# Example below:

curl -X DELETE http://127.0.0.1:5000/api/v1.0/questions/8
returns {"deleted":8,"success":true} or
{"error":404,"message":"resources not found","success":false}

## 4. POST '/api/v1.0/questions'

This endpoint POST a new question, which will require the question and answer text, category, and difficulty score.

For example:
curl --data "{'question': 'test Question? ', 'answer': 'unit testing','difficulty': 4, 'category': '5'}" -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/v1.0/questions/  
 returns {success: True}

## 5. GET '/api/v1.0/categories/<int:id>/questions'

This is GET endpoint to get all questions based on category, it returns True or False based on request and response for example:

{
"current_category" : "Science",
"questions" : [
{
"answer" : "A TECH SCOLARSHIP PROGRAMME",
"category" : "2",
"difficulty" : 2,
"id" : 4,
"question" : "WHAT IS ALXT UDACITY ?"
}
],
"success" : true,
"total_questions" : 1
}

## 6. POST '/api/v1.0/search'

POST endpoint to get questions based on a search term.
It Return any questions for whom the search term
For example:

curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"Unit"}' http://127.0.0.1:5000/api/v1.0/search |json_pp will return :

{
"current_categroy" : "Academy",
"questions" : [
{
"answer" : "unit testing",
"category" : "5",
"difficulty" : 4,
"id" : 80,
"question" : "Why Unit Testing? "
}
],
"success" : true
}

## 6. POST '/api/v1.0/play'

POST endpoint to get questions to play the quiz.
This endpoint takes category and previous question parameters
and return a random questions within the given category,
if provided, and that is not one of the previous questions

using Curl:

curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":[18,19],"quiz_category":{"id":"1", "type":"Academy"} }' http://127.0.0.1:5000/api/v1.0/play json_pp
returns

{
"question" : {
"answer" : "12",
"category" : "1",
"difficulty" : 1,
"id" : 1,
"question" : "WHAT IS 7 + 5 ?"
},
"success" : true
}

## ---[O]> OTHER INFORMATION ON STARTING THE APPLICATION <[0]---

### Backend

These are the major files in the backend:

1. _./backend/flaskr/`__init__.py`_
2. _./backend/test_flaskr.py_
   > View the [README within ./backend for more details.](./frontend/README.md)

### Frontend

1. _./frontend/src/components/QuestionView.js_
2. _./frontend/src/components/FormView.js_
3. _./frontend/src/components/QuizView.js_
   > View the [README within ./frontend for more details.](./frontend/README.md)

## To start the Application - BACKEND

1. cd into backend
2. create virtual environment i.e python3 -m venv env
3. pip Install the requirements.txt example - pip install -r requirments
4. set the FLASK_APP i.e export FLASK_APP=flaskr/**init**.py
5. set the Enviroment to 'Development i.e 'export FLASK_ENV=development
6. Run the app - flask run

## To start the Application - FrontEnd
1. cd into frontend

2. cmd npm install
3. To run frontend application npm start
