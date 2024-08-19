from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from openai import OpenAI
import os
import logging

app = Flask(__name__)
app.secret_key = 'griffin'
client = OpenAI(api_key=API_KEY)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

questions = [
    {
        'question': 'What will be the output of print(type(1/2)) in Python 3?',
        'options': ['<class \'int\'>', '<class \'float\'>', '<class \'double\'>', '<class \'fraction\'>'],
        'correct': '<class \'float\'>'
    },
    {
        'question': 'Which of the following is not a valid variable name in Python?',
        'options': ['my_var', '_myvar', '1var', 'Myvar'],
        'correct': '1var'
    },
    {
        'question': 'What does the following code print? \nfor i in range(5):\n    print(i)',
        'options': ['0 1 2 3 4', '1 2 3 4 5', '0 1 2 3 4 5', '1 2 3 4'],
        'correct': '0 1 2 3 4'
    }
]

post_survey_questions = [
    {
        'question': 'How confident do you feel about your answer?',
        'options': ['Not at all', 'Slightly', 'Moderately', 'Very', 'Extremely']
    },
    {
        'question': 'How much do you trust the information presented in this question?',
        'options': ['Not at all', 'Slightly', 'Moderately', 'Very much', 'Completely']
    }
]

final_survey_questions = [
    {
        'question': 'Overall, how much did you trust the information presented in this quiz?',
        'options': ['Not at all', 'Slightly', 'Moderately', 'Very much', 'Completely']
    },
    {
        'question': 'How helpful was the chatbot in answering the questions?',
        'options': ['Not at all helpful', 'Slightly helpful', 'Moderately helpful', 'Very helpful', 'Extremely helpful']
    }
]


@app.route('/')
def index():
    session.clear()
    session['question_index'] = 0
    session['chat_history'] = []
    session['post_survey_answers'] = []
    return render_template('index.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'question_index' not in session:
        session['question_index'] = 0
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == 'POST':
        if 'answer' in request.form:
            session['last_answer'] = request.form['answer']
            return redirect(url_for('post_survey'))

    if session['question_index'] < len(questions):
        question = questions[session['question_index']]
        return render_template('question.html', question=question, question_number=session['question_index'] + 1,
                               chat_history=session['chat_history'])
    else:
        return redirect(url_for('final_survey'))


@app.route('/chat', methods=['POST'])
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
        app.logger.error(f"OpenAI API error: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/post_survey', methods=['GET', 'POST'])
def post_survey():
    if request.method == 'POST':
        confidence = request.form.get('confidence')
        trust = request.form.get('trust')
        if confidence and trust:
            session.setdefault('post_survey_answers', []).append({'confidence': confidence, 'trust': trust})

        session['question_index'] = session.get('question_index', 0) + 1
        if session['question_index'] >= len(questions):
            return redirect(url_for('final_survey'))
        return redirect(url_for('quiz'))

    return render_template('survey.html', questions=post_survey_questions, survey_type='Post-Question')


@app.route('/final_survey', methods=['GET', 'POST'])
def final_survey():
    if request.method == 'POST':
        overall_trust = request.form.get('overall_trust')
        chatbot_helpfulness = request.form.get('chatbot_helpfulness')
        if overall_trust and chatbot_helpfulness:
            session['final_survey_answers'] = {'overall_trust': overall_trust,
                                               'chatbot_helpfulness': chatbot_helpfulness}
        return redirect(url_for('thank_you'))

    return render_template('survey.html', questions=final_survey_questions, survey_type='Final')


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html', chat_history=session['chat_history'])


if __name__ == '__main__':
    app.run(debug=True)