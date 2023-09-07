from flask import Flask, render_template, request
from utils.src.ask_question_to_pdf import ask_question_to_pdf
from utils.src.ask_question_to_pdf import ask_question_to_user
from utils.src.ask_question_to_pdf import ask_question_to_user_u
from utils.src.ask_question_to_pdf import evaluate_answer
from utils.src.ask_question_to_pdf import read_file

import os

app = Flask(__name__)

# Define your routes and functions


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/prompt", methods=["POST"])
def answer():
    answer = ask_question_to_pdf(request.form["prompt"])
    return {"answer": answer}


@app.route("/upload", methods=["POST"])
def upload_file():
    global uploaded_file_path  # Access the global variable
    if "file_u" not in request.files:
        return "Aucun fichier n'a été téléchargé."

    file_u = request.files["file_u"]

    if file_u.filename == "":
        return "Aucun fichier sélectionné."

    # Save the uploaded file to a specific directory
    upload_folder = os.path.join(os.path.dirname(__file__), "uploads")
    os.makedirs(upload_folder, exist_ok=True)
    file_u.save("file_path")

    # Store the file path in the global variable
    # uploaded_file_path = file_path

    return "Le fichier {} a été téléchargé avec succès.".format(file_u.filename)


@app.route("/question", methods=["GET"])
def question():
    question = ask_question_to_user()
    return {"answer": question}


@app.route("/question", methods=["POST"])
def question_u():
    global uploaded_file_path  # Access the global variable
    if not uploaded_file_path:
        return "Aucun fichier n'a été téléchargé."

    document_u = read_file(
        uploaded_file_path
    )  # Use the file path stored in the global variable
    question = ask_question_to_user_u(document_u)
    return {"answer": question}


@app.route("/answer", methods=["POST"])
def reply():
    user_answer = request.form["prompt"]  # user's answer
    question = request.form["question"]  # original question (thanks .js)

    # using ai to evaluate the user's answer
    evaluation = evaluate_answer(question, user_answer)

    return {"answer": evaluation}


@app.route("/", methods=["GET", "POST"])
def form():
    return render_template("index.html")
