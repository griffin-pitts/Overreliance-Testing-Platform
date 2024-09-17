import os
import logging
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, flash
from .utils.db import insert_user_response
from .utils.questions import questions, post_survey_questions, final_survey_questions
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

main_bp = Blueprint('main', __name__)

# Load .env variables
load_dotenv(find_dotenv())

# Set variables
client = OpenAI(api_key=os.getenv('API_KEY'))

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@main_bp.route('/')
def index():
    session.clear()
    session['question_index'] = 0
    session['answers'] = []
    session['post_survey_answers'] = []
    session['fianl_survey_answers'] = []
    session['chat_history'] = []
    session['user'] = []
    session['user_id'] = []
    return render_template('index.html')

@main_bp.route('/consent')
def collect_consent():
    return render_template('consent.html')

@main_bp.route('/validate_email', methods=['POST'])
def validate_email():
    email = request.form.get('email')
    user_id = request.form.get('id_number')
    
    if not email:
        flash('Email is required', 'error')
        return redirect(url_for('index'))
    
    # Check if email ends with .edu
    if not email.endswith('ufl.edu'):
        flash('Please enter a valid ufl.edu email address', 'error')
        return redirect(url_for('main.index'))
    
    # Redirect to the quiz page if the email is valid
    session['user'] = email
    if user_id:
        session['user_id'] = user_id
    return redirect(url_for('main.collect_consent'))  # Change 'quiz' to the route that handles the quiz


@main_bp.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'question_index' not in session:
        session['question_index'] = 0
    if 'chat_history' not in session:
        session['chat_history'] = []
    if 'answers' not in session:
        session['answers'] = []

    if request.method == 'POST':
        if 'answer' in request.form:
            session['last_answer'] = request.form['answer']
            session['answers'].append(session['last_answer'])
            return redirect(url_for('main.post_survey'))

    if session['question_index'] < len(questions):
        question = questions[session['question_index']]
        return render_template('question.html', question=question, question_number=session['question_index'] + 1,
                               chat_history=session['chat_history'])
    else:
        return redirect(url_for('main.final_survey'))
        


@main_bp.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150
        )
        bot_response = response.choices[0].message.content

        session['chat_history'] = session.get('chat_history', [])
        session['chat_history'].append(('User', user_message))
        session['chat_history'].append(('Bot', bot_response))

        return jsonify({"response": bot_response})
    except Exception as e:
        main_bp.logger.error(f"OpenAI API error: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@main_bp.route('/post_survey', methods=['GET', 'POST'])
def post_survey():
    if request.method == 'POST':
        confidence = request.form.get('confidence')
        trust = request.form.get('trust')
        if confidence and trust:
            session.setdefault('post_survey_answers', []).append({'confidence': confidence, 'trust': trust})

        session['question_index'] = session.get('question_index', 0) + 1
        if session['question_index'] >= len(questions):
            return redirect(url_for('main.final_survey'))
        return redirect(url_for('main.quiz'))

    return render_template('survey.html', questions=post_survey_questions, survey_type='Post-Question')


@main_bp.route('/final_survey', methods=['GET', 'POST'])
def final_survey():
    if request.method == 'POST':
        

        overall_trust = request.form.get('overall_trust')
        chatbot_helpfulness = request.form.get('chatbot_helpfulness')
        if overall_trust and chatbot_helpfulness:
            session['final_survey_answers'] = {'overall_trust': overall_trust,
                                               'chatbot_helpfulness': chatbot_helpfulness}
        
        # Database data preparation
        #TODO
        # Database insert
        # insert_user_response('66bf718f19aab530b26cd132', session['answers'])
        print(session['user'])
        if session['user_id']:
            print(session['user_id'])
        print(session['answers'])
        print(session['post_survey_answers'])
        print(session['final_survey_answers'])

        return redirect(url_for('main.thank_you'))

    return render_template('survey.html', questions=final_survey_questions, survey_type='Final')


@main_bp.route('/thank_you')
def thank_you():
    return render_template('thank_you.html', chat_history=session['chat_history'])

