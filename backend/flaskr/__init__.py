import os
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Question, Category, db


QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


"""
1.  Set up CORS.
"""


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """ 2.  after_request decorator to set Access-Control-Allow """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'content-type,authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    """ 3. GET requests  for all available categories."""
    @app.route('/api/v1.0/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()
            if not categories:
                abort(422)
            return jsonify({
                "success": True,
                "categories": {cat.id: cat.type for cat in categories}
            })
        except Exception as e:
            print(e)
            abort(404)

    [
        {
            'id': 1,
            'question': 'WHAT IS 7 + 5 ?',
            'answer': '12',
            'category': '1',
            'difficulty': 1
        },
        {
            'id': 2, 'question': 'WHO IS JEFF BESOS',
            'answer': 'AMAZON FOUNDER',
            'category': '1',
            'difficulty': 1
        },
    ]

    """ 4. GET requests including pagination (every 10 questions). """
    @app.route('/api/v1.0/questions', methods=['GET'])
    def get_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            categories = Category.query.all()
            current_questions = paginate_questions(request, questions)

            if (len(current_questions) == 0):
                abort(404)

            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions),
                "current_category": current_questions[0]['category'],
                "categories": {cat.id: cat.type for cat in categories}
            })
        except Exception as e:
            print(e)
            abort(404)

    """5. endpoint to DELETE question using a question ID """
    @app.route('/api/v1.0/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.filter(Question.id == id).one_or_none()
        if not question:
            abort(404)
        try:
            question.delete()
            return jsonify({
                'success': True,
                'deleted': id})
        except Exception as e:
            # print(e)
            abort(402)

    """6. Endpoint to POST a new question"""
    @app.route('/api/v1.0/questions', methods=['POST'])
    def add_question():
        try:
            data = request.get_json()
            question = data.get('question')
            answer = data.get('answer')
            difficulty = data.get('difficulty')
            category = data.get('category')

            if ((question is None) or (answer is None)
                    or (difficulty is None) or (category is None)):
                abort(422)

            question = Question(question=question, answer=answer,
                                difficulty=difficulty, category=category)
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id})

        except Exception as e:
            print(e)
            abort(422)

    """ 7. Endpoint to get questions based on category """
    @app.route('/api/v1.0/categories/<id>/questions', methods=['GET'])
    def get_questions_by_category(id):
        try:
            category = Category.query.filter_by(id=id).first()
            sel = Question.query.filter_by(id=int(category.id))
            question_paginate = paginate_questions(request, sel)

            return jsonify({
                'success': True,
                'questions': question_paginate,
                'total_questions': len(Question.query.all()),
                'current_category': category.format()['type']
            })
        except Exception as e:
            print(e)
            abort(500)

    """ 7. Endpoint to search a question """
    @app.route('/api/v1.0/search', methods=['POST'])
    def search_question():
      try:

        body = request.get_json()
        search_term = body.get('searchTerm', None)      
        if not search_term:
          return jsonify({
              'success': True,
              'questions': [],
              'current_category': ""
          })

        questions = Question.query.order_by(Question.id).filter(
                      Question.question.ilike('%{}%'.format(search_term))
                  ).all()  
        current_questions = paginate_questions(request, questions)
        categories = [category.format() for category in Category.query.order_by(Category.id).all()]
        
        return jsonify({
                          'success': True,
                          'questions': current_questions,
                          'current_category': current_questions[0]['category']
                      })
      except:
        abort(404)
          


    """ 7. Endpoint to play Trivia question """
    @app.route('/api/v1.0/play', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()
            body = request.get_json()
            previous_questions = body.get("previous_questions", None)
            quiz_category = body.get("quiz_category", None)
            if quiz_category:
                if quiz_category['id'] == 0:
                    question = Question.query.order_by(Question.id).filter(
                        Question.id.notin_(previous_questions)).first()
                else:
                    question = Question.query.order_by(Question.id).filter(
                        Question.id.notin_(previous_questions)).filter(Question.category == quiz_category['id']).first()

                if previous_questions is None:
                    previous_questions = []

                if question:
                    previous_questions.append(question.id)

            return jsonify({
                "success": True,
                "previous_questions": previous_questions,
                "question": question.format() if question else question
            })
        except:
            abort(422)

    """ Error Handler 404 """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "resources not found"
        }), 404

    """ Error Handler 422 """
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "unprocessable"
        }), 422

    """ Error Handler 400 """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "bad request"
        }), 400

    """ Error Handler 500 """
    @app.errorhandler(500)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500

    if __name__ == '__main__':
        app.run(debug=True)

    return app
