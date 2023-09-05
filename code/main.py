from flask import Flask, render_template, request
from utils.src.ask_question_to_pdf import ask_question_to_pdf
from utils.src.ask_question_to_pdf import ask_question_to_user

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
