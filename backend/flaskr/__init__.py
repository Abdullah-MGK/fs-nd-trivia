import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
#from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  




  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''





  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by('type').all()

    return jsonify({
      'categories': [category.format() for category in categories]
    })
  
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  
  @app.route('/questions', methods=['GET'])
  def get_questions():
    questions = Question.query.all()
    total_questions = len(questions)
    categories_id = {question.category for question in questions}
    
    return jsonify({
      'questions': [question.format() for question in questions],
      'totalQuestions': total_questions,
      'categories': list(categories_id),
      'currentCategory': ''
    })
  





  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
  
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    return jsonify({
      'success':False
    })




  
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  
  @app.route('/questions', methods=['POST'])
  def post_question():
    return jsonify({
      'success':False
    })




  
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 
  
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    search_term = 'autobiography'
    result_questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
    total_questions = len(result_questions)
    categories_id = {question.category for question in result_questions}
    
    return jsonify({
      'questions': [question.format() for question in result_questions],
      'totalQuestions': 0,
      'categories': list(categories_id),
      'currentCategory': ''
    })





  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 
  
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    questions = Question.query.filter_by(category=category_id).all()
    total_questions = len(questions)
    
    return jsonify({
      'questions': [question.format() for question in questions],
      'totalQuestions': total_questions,
      'currentCategory': category_id
    })
  




  
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  
  @app.route('/<int:category_id>/<int:previous_question>/question', methods=['POST'])
  def get_next_question(category_id, previous_question):
    return jsonify({
      'question': '',
      'answer': ''
    })




  
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Not found"
      }), 404
  
  return app
