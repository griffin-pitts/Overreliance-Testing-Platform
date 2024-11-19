# Necessary imports
import os
import random
import json
# import logging
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, flash
from .utils.db import insert_user_response
from .utils.questions import questions, get_initial_recommendation, get_chat_prompt, post_survey_questions, final_survey_questions
from .utils.demographics import demographics_questions
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# Initialize variable
main_bp = Blueprint('main', __name__)

# Load environment variable
load_dotenv(find_dotenv())

# Set environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
# Set up logging
# logging.basicConfig(level=logging.DEBUG)

@main_bp.route('/')
def index():
    session.clear()
    all_indices = list(range(len(questions)))
    misleading_indices = [i for i, q in enumerate(questions) if q['is_misleading']]
    normal_indices = [i for i, q in enumerate(questions) if not q['is_misleading']]
    random.shuffle(misleading_indices)
    random.shuffle(normal_indices)
    session['question_order'] = misleading_indices + normal_indices
    session['question_index'] = 0
    session['answers'] = []
    session['post_survey_answers'] = []
    session['final_survey_answers'] = []
    session['chat_history'] = []
    session['user'] = []
    session['user_id'] = []
    return render_template('index.html')

@main_bp.route('/consent', methods=['GET', 'POST'])
def collect_consent():
    if request.method == 'POST':
        if request.form.get('consent'):
            session['consented'] = True
            return redirect(url_for('main.collect_demographics'))
        return redirect(url_for('main.index'))
    return render_template('consent.html')

@main_bp.route('/demographics', methods=['GET', 'POST'])
def collect_demographics():
    if request.method == 'POST':
        demographics_data = {
            'age_category': request.form.get('age_category'),
            'gender': request.form.get('gender'),
            'ethnicity': request.form.getlist('ethnicity'),
            'ai_usage': request.form.get('ai_usage'),
            'ai_frequency': request.form.get('ai_frequency'),
            'ai_use_type': request.form.getlist('ai_use_type'),
            'academic_level': request.form.get('academic_level'),
            'major_category': request.form.get('major_category'),
            'gpa': request.form.get('gpa'),
            'programming_education': request.form.get('programming_education'),
            'courses_completed': request.form.get('courses_completed'),
            'practical_experience': request.form.get('practical_experience'),
            'learning_preference': request.form.get('learning_preference'),
            'problem_solving': request.form.get('problem_solving'),
            'study_time': request.form.get('study_time')
        }
        session['demographics'] = demographics_data
        return redirect(url_for('main.pre_survey'))

    return render_template('demographics.html')

@main_bp.route('/validate_email', methods=['POST'])
def validate_email():
    email = request.form.get('email')
    user_id = request.form.get('id_number')
    
    if not email:
        flash('Email is required', 'error')
        return redirect(url_for('index'))
    
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
    if 'question_order' not in session:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        if 'answer' in request.form:
            current_q_index = session['question_order'][session['question_index']]
            answer_data = {
                'question_index': current_q_index,
                'answer': request.form['answer'],
                'is_misleading': questions[current_q_index]['is_misleading'],
                'correct_answer': questions[current_q_index]['correct']
            }
            session['answers'].insert(session['question_index'], answer_data)
            #print(session['question_order'])
            print(session['question_index'])
            #session['tracker'] += 1
            
            # Add divider to chat history
            session['chat_history'] = session.get('chat_history', [])
            session['chat_history'].append(('Divider', f"――――――― End of Question {session['question_index'] + 1} ―――――――"))
            
            return redirect(url_for('main.post_survey'))

    if session['question_index'] < len(session['question_order']):
        current_q_index = session['question_order'][session['question_index']]
        question = questions[current_q_index]
        return render_template('question.html', 
                             question=question,
                             question_number=session['question_index'] + 1,
                             total_questions=len(questions),
                             chat_history=session.get('chat_history', []))
    else:
        return redirect(url_for('main.final_survey'))
        
@main_bp.route('/get_initial_recommendation', methods=['GET'])
def initial_recommendation():
    if 'question_order' not in session:
        return jsonify({"error": "No active question"}), 400
    
    current_q_index = session['question_order'][session['question_index']]
    recommendation = get_initial_recommendation(current_q_index)
    user_message = "What's your recommended answer to this question?"

    session['chat_history'] = session.get('chat_history', [])
    session['chat_history'].append(('User', user_message))
    session['chat_history'].append(('Assistant', recommendation['recommendation']))

    return jsonify(recommendation)

@main_bp.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if 'question_order' not in session:
        return jsonify({"error": "No active question"}), 400
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        current_q_index = session['question_order'][session['question_index']]
        chat_prompt = get_chat_prompt(current_q_index)
        
        system_message = f"{chat_prompt['system_context']}\n\nQuestion Context: {chat_prompt['question_context']}\nStance: {chat_prompt['stance']}"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
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

import random

def get_pre_survey_questions():
    questions = [
        # Programming Self-Efficacy
        {"id": "independent_programming", "text": "I am confident in my ability to program independently"},
        {"id": "learn_languages", "text": "I can learn new programming languages independently"},
        {"id": "identify_improvements", "text": "I can identify when my code needs improvement"},
        
        # General Trust in AI
        {"id": "ai_dependability", "text": "When working with an AI assistant while programming, I feel I can depend on the AI assistant"},
        {"id": "ai_reliability", "text": "I can rely on AI for effective assistance with coding tasks"},
        {"id": "ai_explanation", "text": "I feel I can count on AI to explain programming concepts clearly"},
        
        # Concerns for trust
        {"id": "ai_dependency", "text": "I worry about becoming too dependent on AI"},
        {"id": "incorrect_advice", "text": "I am concerned that AI might give me incorrect advice"},
        {"id": "blind_trust", "text": "I feel uncertain about blindly trusting AI's suggestions"},
        {"id": "learning_hindrance", "text": "I worry that using AI might hinder my learning"},
        
        # Need for Cognition
        {"id": "code_understanding", "text": "I enjoy understanding how code works rather than just getting it to work"},
        {"id": "solution_exploration", "text": "I like exploring different solutions to programming problems"},
        {"id": "concept_understanding", "text": "I seek to understand the underlying concepts when learning programming"},
        {"id": "self_solving", "text": "I prefer figuring out solutions before asking for help"},
        {"id": "complex_problems", "text": "I enjoy the process of solving complex problems"},
        
        # Programming Literacy
        {"id": "fundamental_concepts", "text": "I understand fundamental programming concepts (variables, loops, functions)"},
        {"id": "code_comprehension", "text": "I can read and comprehend code written by others"},
        {"id": "data_structures", "text": "I can identify and use appropriate data structures"},
        {"id": "oop_principles", "text": "I understand object-oriented programming principles"},
        {"id": "explain_concepts", "text": "I can explain programming concepts to others"},
        {"id": "language_proficiency", "text": "I am proficient in programming in one or more programming languages"},
        
        # AI Literacy
        {"id": "ai_principles", "text": "I understand the basic principles of how AI systems work"},
        {"id": "ai_use_cases", "text": "I can identify appropriate use cases for AI in programming"},
        {"id": "ai_risks", "text": "I understand the risks and biases of AI assistants"},
        {"id": "ai_prompting", "text": "I can effectively prompt AI tools to get desired results"}
    ]
    
    random.shuffle(questions)
    return questions

@main_bp.route('/pre_survey', methods=['GET', 'POST'])
def pre_survey():
    if request.method == 'POST':
        survey_data = {key: request.form[key] for key in request.form}
        session['pre_survey_data'] = survey_data
        return redirect(url_for('main.instructions'))

    questions = get_pre_survey_questions()
    return render_template('pre_survey.html', questions=questions)

@main_bp.route('/instructions', methods=['GET'])
def instructions():
    return render_template('instructions.html')

@main_bp.route('/post_survey', methods=['GET', 'POST'])
def post_survey():
    if request.method == 'POST':
        survey_data = {
            'confidence': request.form.get('confidence'),
            'trust': request.form.get('trust'),
            'helpfulness': request.form.get('helpfulness')
        }
        session.setdefault('post_survey_answers', []).append(survey_data)

        session['question_index'] = session.get('question_index', 0) + 1
        if session['question_index'] >= len(questions):
            return redirect(url_for('main.final_survey'))
        return redirect(url_for('main.quiz'))

    return render_template('post_survey.html')

def get_final_survey_questions():
    questions = [
        # Overreliance Assessment
        {"id": "blind_acceptance", "text": "I found myself accepting the AI's suggestions without fully understanding them"},
        {"id": "questioned_recommendations", "text": "I questioned the AI's recommendations before accepting them"},
        {"id": "immediate_usage", "text": "I developed a habit of immediately using the AI's suggestions"},
        {"id": "verified_answers", "text": "I verified the AI's answers with my own knowledge"},
        
        # Trust in Chatbot
        {"id": "reliable_advice", "text": "The AI provided reliable programming advice"},
        {"id": "trustworthy_explanations", "text": "The AI's explanations were trustworthy"},
        {"id": "count_recommendations", "text": "I could count on the AI's recommendations"},
        {"id": "depend_solving", "text": "I could depend on the AI for help with solving problems"},
        
        # Satisfaction with AI
        {"id": "recommendations_helpful", "text": "The AI's recommendations were helpful"},
        {"id": "explanations_clear", "text": "The AI's explanations were clear and understandable"},
        {"id": "appropriate_responses", "text": "The AI responded appropriately to my questions"},
        {"id": "quality_satisfaction", "text": "I was satisfied with the quality of the AI's assistance"},

        # Decision-Making Process
        {"id": "careful_consideration", "text": "I carefully considered each recommendation before accepting it"},
        {"id": "knowledge_combination", "text": "I combined my knowledge with the AI's suggestions"},
        {"id": "own_decisions", "text": "I made my own decisions after consulting the AI"},
        {"id": "critical_evaluation", "text": "I evaluated the AI's reasoning critically"},
        {"id": "independence", "text": "I maintained independence in my problem-solving"}
    ]
    
    random.shuffle(questions)
    return questions

@main_bp.route('/final_survey', methods=['GET', 'POST'])
def final_survey():
    if request.method == 'POST':
        survey_data = {key: request.form[key] for key in request.form}
        session['final_survey_answers'] = survey_data
        
        # Create combined data for database storage
        combined_data = {
            "email": session.get('user'),
            "uf_id": session.get('user_id'),
            "question_order": session.get('question_order'),
            "answers": session.get('answers'),
            "post_survey_answers": session.get('post_survey_answers'),
            "final_survey_answers": survey_data
        }

        #insert_user_response(combined_data)
        return redirect(url_for('main.thank_you'))

    questions = get_final_survey_questions()
    return render_template('final_survey.html', questions=questions)

@main_bp.route('/thank_you')
def thank_you():
    return render_template('thank_you.html', chat_history=session['chat_history'])
