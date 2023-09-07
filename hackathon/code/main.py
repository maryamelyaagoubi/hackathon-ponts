from flask import Flask, render_template, request
from utils.src.ask_question_to_pdf import ask_question_to_pdf
from utils.src.ask_question_to_pdf import ask_question_to_pdf_u
from utils.src.ask_question_to_pdf import ask_question_to_user
from utils.src.ask_question_to_pdf import ask_question_to_user_u
from utils.src.ask_question_to_pdf import evaluate_answer
from utils.src.ask_question_to_pdf import read_file
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)


# Define your routes and functions


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    global uploaded_file_content  # Stockage du document

    if "file_u" not in request.files:
        return "Aucun fichier n'a été téléchargé."

    file_u = request.files["file_u"]

    if file_u.filename == "":
        return "Aucun fichier sélectionné."

    try:
        file_path = os.path.join(
            os.path.dirname(__file__), secure_filename(file_u.filename)
        )
        file_u.save(file_path)
        uploaded_file_content = read_file(file_path)

        # question = ask_question_to_user_u(read_file(file_path))
        # return {"answer": question}
        return {"answer": "Le fichier a bien été téléchargé !"}

    except Exception as e:
        return (
            "Erreur lors de l'enregistrement ou du traitement du fichier : {}".format(
                str(e)
            )
        )


@app.route("/prompt", methods=["POST"])
def answer():
    if uploaded_file_content is not None:
        answer = ask_question_to_pdf_u(request.form["prompt"], uploaded_file_content)
    else:
        answer = ask_question_to_pdf(request.form["prompt"])
    return {"answer": answer}


@app.route("/question", methods=["GET"])
def question():
    if uploaded_file_content is not None:
        question = ask_question_to_user_u(uploaded_file_content)
    else:
        question = ask_question_to_user()
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
