import os,sys
from re import T
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate, migrate
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  db=setup_db(app)
  migrate=Migrate(app,db)
  
  '''
  Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''
  Use the after_request decorator to set Access-Control-Allow
  '''
    
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response
  '''
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/api/categories/', methods=['GET'])
  def get_all_categories():
    return jsonify({
      'categories':{c.id:c.type for c in Category.query.all()},
      'success':True
    })

  ''' 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/api/questions/')
  def get_all_questions():
    page=int(request.args.get('page',1))
    current_category=request.args.get('category',None)
    try:
      return jsonify({
        'success':True,
        'questions':[q.format() for q in Question.query.paginate(page,QUESTIONS_PER_PAGE).items],
        'total_questions':len(Question.query.all()),
        'current_category':current_category,
        'categories':{c.id:c.type for c in Category.query.all()}
      })
    except Exception as e:
      print(e)
      abort(404)
  '''
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      Question.query.get(question_id).delete()
      return jsonify({
      'success':True
    })
    except Exception as e:
      print(e)
      abort(404)

  '''
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/api/questions', methods=['POST'])
  def insert_question():
    try:
      data= request.json
      question=Question(data['question'],data['answer'],data['category'],data['difficulty'])
      question.insert()
      return jsonify({'success':True})
    except Exception as e:
      print(e)
      abort(422)

  '''
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/api/search/questions', methods=['POST'])
  def search_questions():
    word=request.json.get('searchTerm','')
    current_category=request.json.get('current_category',None)
    result=Question.query.filter(Question.question.ilike('%{}%'.format(word))).all()
    return jsonify({
      'questions':[q.format() for q in result],
      'total_questions':len(result),
      'current_category':current_category
    })

  ''' 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/api/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    try:
      category=Category.query.get(category_id)
      return jsonify({
        'success':True,
        'questions':[q.format() for q in category.questions],
        'total_questions':len(category.questions),
        'current_category':category.type
      })
    except Exception as e:
      print (e)
      abort (404)

  '''
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/api/quizzes', methods=['POST'])
  def quizzes():
    category_id=request.json.get('quiz_category',{'id':0})['id']
    previous_questions=request.json.get('previous_questions',[])
    questions=Question.query
    if category_id!=0:
      questions= questions.filter_by(category=Category.query.get(category_id))
    for ps in previous_questions:
      questions=questions.filter(Question.id!=ps)
    questions=questions.all()
    if len(questions)>0:
      rand=random.randint(0,len(questions)-1)
      question=questions[rand].format()
    else:
      question=None

    return jsonify({
      'question':question,
      'success':True
    })

  '''
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found():
    return jsonify({
      'success':False,
      'message':'Not Found'
    })

  @app.errorhandler(422)
  def request_error():
    return jsonify({
      'success':False,
      'message':'request_error'
    })

  return app

    