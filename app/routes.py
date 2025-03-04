# Necessary imports
import os
import time
import random
import json

# import logging
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    jsonify,
    flash,
)
from .utils.db import insert_user_response, find_user
from .utils.questions import (
    questions,
    get_initial_recommendation,
    get_chat_prompt,
    post_survey_questions,
    final_survey_questions,
)
from .utils.demographics import demographics_questions
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# Initialize variable
main_bp = Blueprint("main", __name__)

# Load environment variable
load_dotenv(find_dotenv())

# Set environment variable
client = OpenAI(api_key=os.getenv("API_KEY"))

# Set up logging
# logging.basicConfig(level=logging.DEBUG)


@main_bp.route("/")
def index():
    session.clear()
    all_indices = list(range(len(questions)))
    misleading_indices = [i for i, q in enumerate(questions) if q["is_misleading"]]
    normal_indices = [i for i, q in enumerate(questions) if not q["is_misleading"]]
    random.shuffle(misleading_indices)
    random.shuffle(normal_indices)
    session["question_order"] = misleading_indices + normal_indices
    random.shuffle(session["question_order"])
    session["pre_survey_data"] = []
    session["question_index"] = 0
    session["answers"] = []
    session["post_survey_answers"] = []
    session["final_survey_answers"] = []
    session["chat_history"] = []
    session["user"] = []
    session["user_id"] = []
    session["firstName"] = []
    session["lastName"] = []
    session["classSchool"] = []
    session["demographics"] = []
    session["times"] = []
    session["begin"] = 0
    session["elapsed_time"] = 0
    session["end_time"] = 0
    session["start_time"] = 0
    
    return render_template("index.html")

@main_bp.route("/email_error")
def email_error():
    return render_template("email_error.html")

@main_bp.route("/consent", methods=["GET", "POST"])
def collect_consent():
    if request.method == "POST":
        if request.form.get("consent"):
            session["consented"] = True
            return redirect(url_for("main.collect_demographics"))
        return redirect(url_for("main.index"))
    return render_template("consent.html")


@main_bp.route("/demographics", methods=["GET", "POST"])
def collect_demographics():
    if request.method == "POST":
        demographics_data = {
            "age_category": request.form.get("age"),
            "gender": request.form.get("gender"),
            "ethnicity": request.form.getlist("ethnicity"),
            "ai_usage": request.form.get("ai_experience"),
            "ai_frequency": request.form.get("ai_frequency"),
            "ai_use_type": request.form.getlist("ai_use_type"),
            "academic_level": request.form.get("year"),
            "major_category": request.form.get("major"),
            "minor_category": request.form.get("minor"),
            "gpa": request.form.get("gpa"),
        }
        session["demographics"] = demographics_data
        return redirect(url_for("main.pre_survey"))

    return render_template("demographics.html")


@main_bp.route("/validate_email", methods=["GET", "POST"])
def validate_email():
    email = request.form.get("email")
    user_id = request.form.get("id_number")
    first_name = request.form.get("firstName")
    last_name = request.form.get("lastName")
    student_class = request.form.get("classSchool")

    if not email:
        return redirect(url_for("main.email_error"))

    # Check if email ends with .edu
    if not email.endswith("ufl.edu"):
        return redirect(url_for("main.email_error"))

    # Redirect to the quiz page if the email is valid
    session["user"] = email
    if user_id:
        session["user_id"] = user_id
        session["firstName"] = first_name
        session["lastName"] = last_name
        session["classSchool"] = student_class

    if find_user(email):
        return redirect(url_for("main.thank_you"))
    
    return redirect(
        url_for("main.collect_consent")
    )  # Change 'quiz' to the route that handles the quiz


@main_bp.route("/quiz", methods=["GET", "POST"])
def quiz():
    def insert_at_index(lst, index, value):
        if index >= len(lst):
            lst.extend([0] * (index - len(lst) + 1))  # Extend the list with 0s
        lst[index] = value

    if "question_order" not in session:
        return redirect(url_for("main.index"))
    
    if session["begin"] == 0:
        session["begin"] = 1
        session["start_time"] = time.time()

    if request.method == "POST":
        if "answer" in request.form:
            current_q_index = session["question_order"][session["question_index"]]
            answer_data = {
                "question_index": current_q_index,
                "answer": request.form["answer"],
                "is_misleading": questions[current_q_index]["is_misleading"],
                "correct_answer": questions[current_q_index]["correct"],
            }

            if session["begin"] == 1:
                session["begin"] = 0
                session["end_time"] = time.time()
                session["elapsed_time"] = session["end_time"] - session["start_time"]

            insert_at_index(
                session["answers"],
                session["question_order"][session["question_index"]],
                answer_data,
            )
            insert_at_index(
                session["times"],
                session["question_order"][session["question_index"]],
                session["elapsed_time"],
            )

            # Add divider to chat history
            session["chat_history"] = session.get("chat_history", [])
            session["chat_history"].append(
                (
                    "Divider",
                    f"――――――― End of Question {session['question_index'] + 1} ―――――――",
                )
            )

            return redirect(url_for("main.post_survey"))

    if session["question_index"] < len(session["question_order"]):
        current_q_index = session["question_order"][session["question_index"]]
        question = questions[current_q_index]
        return render_template(
            "question.html",
            question=question,
            question_number=session["question_index"] + 1,
            total_questions=len(questions),
            chat_history=session.get("chat_history", []),
        )
    else:
        return redirect(url_for("main.final_survey"))
    
    


@main_bp.route("/get_initial_recommendation", methods=["GET"])
def initial_recommendation():
    if "question_order" not in session:
        return jsonify({"error": "No active question"}), 400

    current_q_index = session["question_order"][session["question_index"]]
    recommendation = get_initial_recommendation(current_q_index)
    user_message = "What's your recommended answer to this question?"

    session["chat_history"] = session.get("chat_history", [])
    session["chat_history"].append(("User", user_message))
    session["chat_history"].append(("Assistant", recommendation["recommendation"]))

    return jsonify(recommendation)


@main_bp.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if "question_order" not in session:
        return jsonify({"error": "No active question"}), 400

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        current_q_index = session["question_order"][session["question_index"]]
        chat_prompt = get_chat_prompt(current_q_index)

        system_message = f"{chat_prompt['system_context']}\n\nQuestion Context: {chat_prompt['question_context']}\nStance: {chat_prompt['stance']}"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            max_tokens=150,
        )
        bot_response = response.choices[0].message.content

        session["chat_history"] = session.get("chat_history", [])
        session["chat_history"].append(("User", user_message))
        session["chat_history"].append(("Assistant", bot_response))

        return jsonify({"response": bot_response})
    except Exception as e:
        main_bp.logger.error(f"OpenAI API error: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@main_bp.route("/pre_survey", methods=["GET", "POST"])
def pre_survey():
    if request.method == "POST":
        survey_data = {
            "independent_programming": request.form.get("independent_programming"),
            "learn_languages": request.form.get("learn_languages"),
            "identify_improvements": request.form.get("identify_improvements"),
            "ai_dependability": request.form.get("ai_dependability"),
            "ai_reliability": request.form.get("ai_reliability"),
            "ai_explanation": request.form.get("ai_explanation"),
            "ai_dependency": request.form.get("ai_dependency"),
            "incorrect_advice": request.form.get("incorrect_advice"),
            "blind_trust": request.form.get("blind_trust"),
            "learning_hindrance": request.form.get("learning_hindrance"),
            "code_understanding": request.form.get("code_understanding"),
            "solution_exploration": request.form.get("solution_exploration"),
            "concept_understanding": request.form.get("concept_understanding"),
            "self_solving": request.form.get("self_solving"),
            "complex_problems": request.form.get("complex_problems"),
            "fundamental_concepts": request.form.get("fundamental_concepts"),
            "code_comprehension": request.form.get("code_comprehension"),
            "data_structures": request.form.get("data_structures"),
            "oop_principles": request.form.get("oop_principles"),
            "explain_concepts": request.form.get("explain_concepts"),
            "language_proficiency": request.form.get("language_proficiency"),
            "ai_principles": request.form.get("ai_principles"),
            "ai_use_cases": request.form.get("ai_use_cases"),
            "ai_risks": request.form.get("ai_risks"),
            "ai_prompting": request.form.get("ai_prompting"),
            "ai_classroom_concerns": request.form.get("ai_classroom_concerns"),
        }
        session["pre_survey_data"] = survey_data
        return redirect(url_for("main.instructions"))

    return render_template("pre_survey.html")


@main_bp.route("/instructions", methods=["GET"])
def instructions():
    return render_template("instructions.html")


@main_bp.route("/post_survey", methods=["GET", "POST"])
def post_survey():
    if request.method == "POST":
        survey_data = {
            "confidence": request.form.get("confidence"),
            "trust": request.form.get("trust"),
            "helpfulness": request.form.get("helpfulness"),
        }
        session.setdefault("post_survey_answers", []).append(survey_data)

        session["question_index"] = session.get("question_index", 0) + 1
        if session["question_index"] >= len(questions):
            return redirect(url_for("main.final_survey"))
        return redirect(url_for("main.quiz"))

    return render_template("post_survey.html")


@main_bp.route("/final_survey", methods=["GET", "POST"])
def final_survey():
    if request.method == "POST":
        survey_data = {
            "blind_acceptance": request.form.get("blind_acceptance"),
            "questioned_recommendations": request.form.get("questioned_recommendations"),
            "immediate_usage": request.form.get("immediate_usage"),
            "verified_answers": request.form.get("verified_answers"),
            "reliable_advice": request.form.get("reliable_advice"),
            "trustworthy_explanations": request.form.get("trustworthy_explanations"),
            "count_recommendations": request.form.get("count_recommendations"),
            "depend_solving": request.form.get("depend_solving"),
            "recommendations_helpful": request.form.get("recommendations_helpful"),
            "explanations_clear": request.form.get("explanations_clear"),
            "appropriate_responses": request.form.get("appropriate_responses"),
            "quality_satisfaction": request.form.get("quality_satisfaction"),
            "careful_consideration": request.form.get("careful_consideration"),
            "knowledge_combination": request.form.get("knowledge_combination"),
            "own_decisions": request.form.get("own_decisions"),
            "critical_evaluation": request.form.get("critical_evaluation"),
            "independence": request.form.get("independence"),
        }
        session["final_survey_answers"] = survey_data

        #print("Session Data Summary:")
        #print(f"email: {session.get('user')}")
        #print(f"uf id: {session.get('user_id')}")
        #print(f"Question Order: {session.get('question_order')}")
        #print(f"Answers: {session.get('answers')}")
        #print(f"Post-survey answers: {session.get('post_survey_answers')}")
        #print(f"Final survey answers: {session.get('final_survey_answers')}")

        # Create an empty dictionary to hold all the data
        combined_data = {}

        # Add each data element to the dictionary
        combined_data["email"] = session.get("user")
        combined_data["uf_id"] = session.get("user_id")
        combined_data["question_order"] = session.get("question_order")
        combined_data["answers"] = session.get("answers")
        combined_data["pre_survey_answers"] = session.get("pre_survey_data")
        combined_data["post_survey_answers"] = session.get("post_survey_answers")
        combined_data["final_survey_answers"] = session.get("final_survey_answers")
        combined_data["chat_history"] = session.get("chat_history")
        combined_data["firstName"] = session.get("firstName")
        combined_data["lastName"] = session.get("lastName")
        combined_data["classSchool"] = session.get("classSchool")
        combined_data["demographics"] = session.get("demographics")
        combined_data["times"] = session.get("times")

        #print(f"Demographics answers: {session.get('demographics')}")

        insert_user_response(combined_data)

        return redirect(url_for("main.thank_you"))

    return render_template("final_survey.html")


@main_bp.route("/thank_you")
def thank_you():
    return render_template("thank_you.html", chat_history=session["chat_history"])
