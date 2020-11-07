import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
#from flask_cors import CORS
import random

from models import setup_db, Question, Category, db






QUESTIONS_PER_PAGE = 10
def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  #questions = [question.format() for question in selection]
  current_questions = selection[start:end]
  
  return current_questions





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
    try:
      categories = Category.query.order_by('type').all()  
      return jsonify({'success':True,
      'categories':{category.id:category.type for category in categories}
      })
    
    except:
      abort(500)
  




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
    try:
      all_questions = Question.query.order_by(Question.id).all()
      total_questions = len(all_questions)
      
      questions = paginate_questions(request, all_questions)
      if len(questions) == 0:
        abort(404)
      
      categories = Category.query.order_by('type').all()
      
      return jsonify({
        'success':True,
        'questions': [question.format() for question in questions],
        'totalQuestions': total_questions,
        'categories': {category.id:category.type for category in categories},
        'currentCategory': ''
      })

    except:
      abort(500)




  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
  
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      
      if question is None:
        abort(404)
      try:
        question.delete()
        db.session.commit()
        db.session.close()
      except:
        db.session.rollback()
        db.session.close()
        abort(500)
      return jsonify({
        'success':False,
        'deleted_question':question_id
      })
    except:
      abort(422)




  
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
  def add_question():
    #data = request.get_json() or None
    #print(data, file = sys.stderr)
    try:
      question = request.json.get('question')
      answer = request.json.get('answer')
      category = request.json.get('category')
      difficulty = request.json.get('difficulty')
    
    except:
      print("in except", file = sys.stderr)
      abort(400)

    if not (question and answer and category and difficulty):
      print("in if", file = sys.stderr)
      abort(422)

    try:
      new_question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
      new_question.insert()
    except:
      db.session.rollback()
      abort(500)
    
    return jsonify({
      'success':True,
      'question':new_question.format()
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
    try:
      search_term = request.json.get('search_term')
    
    except:
      print("in except", file = sys.stderr)
      abort(400)
    
    if not (search_term):
      print("in if", file = sys.stderr)
      abort(422)
    
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
    try:
      questions = Question.query.filter_by(category=category_id).all()
    except:
      abort(500)
    
    return jsonify({
      'success':True,
      'questions': [question.format() for question in questions],
      'totalQuestions': len(questions),
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
  
  @app.route('/quizzes', methods=['POST'])
  def get_next_question():
    try:
      previous_questions_query = request.json.get('previous_questions')
      previous_questions = [int(question) for question in previous_questions_query]
      quiz_category_query = request.json.get('quiz_category')
      quiz_category = quiz_category_query['id']
    except:
      abort(400)
    
    categories = Category.query.order_by(Category.type).all()
    categories_id = [category.id for category in categories]
    
    if quiz_category == 0:
      questions = Question.query.order_by(Question.id).all()
    elif quiz_category not in categories_id:
      questions = Question.query.filter_by(category=quiz_category).all()
    else:
      abort(404)
    
    try:
      questions = [question.format() for question in questions]
      random.shuffle(questions)
      finished = False
      for question in questions:
        print(previous_questions, file = sys.stderr)
        print(question, file = sys.stderr)
        print(question['id'], file = sys.stderr)
        if question['id'] not in previous_questions:
          print("true", file = sys.stderr)
          current_question = question
          finished = True
          break
        else:
          print("false", file = sys.stderr)
      if not finished:
        current_question = ""
    
    except:
      abort(500)
    
    return jsonify({
      'success':True,
      'question':current_question
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
