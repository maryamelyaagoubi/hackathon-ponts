from flask import Flask, render_template, request
from utils.src.ask_question_to_pdf import ask_question_to_pdf
from utils.src.ask_question_to_pdf import ask_question_to_user
from utils.src.ask_question_to_pdf import evaluate_answer

app = Flask(__name__)

# Define your routes and functions

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/prompt',methods=["POST"])
def answer():
	answer = ask_question_to_pdf(request.form['prompt'])
	return {"answer":answer}

@app.route('/question',methods=["GET"])
def question():
	question = ask_question_to_user()
	return {"answer":question}

@app.route('/answer', methods=["POST"])
def reply():
    user_answer = request.form['prompt']  # user's answer 
    question = request.form['question']    # original question (thanks .js)
    
    # using ai to evaluate the user's answer
    evaluation = evaluate_answer(question, user_answer)
    
    return {"answer": evaluation}
