from io import StringIO
import os
import fitz
import openai
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize

load_dotenv()


def open_file(filepath):
    with open(filepath, "r", encoding="utf-8") as infile:
        return infile.read()


openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")


def read_pdf(filename):
    context = ""

    # Open the PDF file
    with fitz.open(filename) as pdf_file:
        # Get the number of pages in the PDF file
        num_pages = pdf_file.page_count

        # Loop through each page in the PDF file
        for page_num in range(num_pages):
            # Get the current page
            page = pdf_file[page_num]

            # Get the text from the current page
            page_text = page.get_text().replace("\n", "")

            # Append the text to context
            context += page_text
    return context


def read_txt(filename):
    context = ""
    # Open the text file
    with open(filename, "r", encoding="utf-8") as txt_file:
        # Get the text from the text file
        context = txt_file.read()
    return context


def split_text(text, chunk_size=5000):
    """
    Splits the given text into chunks of approximately the specified chunk size.

    Args:
    text (str): The text to split.

    chunk_size (int): The desired size of each chunk (in characters).

    Returns:
    List[str]: A list of chunks, each of approximately the specified chunk size.
    """

    chunks = []
    current_chunk = StringIO()
    current_size = 0
    sentences = sent_tokenize(text)
    for sentence in sentences:
        sentence_size = len(sentence)
        if sentence_size > chunk_size:
            while sentence_size > chunk_size:
                chunk = sentence[:chunk_size]
                chunks.append(chunk)
                sentence = sentence[chunk_size:]
                sentence_size -= chunk_size
                current_chunk = StringIO()
                current_size = 0
        if current_size + sentence_size < chunk_size:
            current_chunk.write(sentence)
            current_size += sentence_size
        else:
            chunks.append(current_chunk.getvalue())
            current_chunk = StringIO()
            current_chunk.write(sentence)
            current_size = sentence_size
    if current_chunk:
        chunks.append(current_chunk.getvalue())
    return chunks


filename = os.path.join(os.path.dirname(__file__), "filename.pdf")


def read_file(filename):
    # Get the file extension
    file_extension = os.path.splitext(filename)[-1].lower()

    if file_extension == ".pdf":
        document = read_pdf(filename)
    elif file_extension == ".txt":
        document = read_txt(filename)
    return document


chunks = split_text(document)
text = "La terre s'est aplatie à cause des ours"


def gpt3_completion(question, prompt_eng):
    reponse = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
            {"role": "assistant", "content": prompt_eng},
        ],
    )
    answer = reponse["choices"][0]["message"]["content"]
    return answer


def ask_question_to_pdf(question):
    return gpt3_completion(question, document)


def ask_question_to_user_u(doc):
    return gpt3_completion(
        "Poses moi une question à propos du texte que j'ai fourni", doc
    )


def ask_question_to_user():
    return ask_question_to_user_u(document)


def evaluate_answer(question, user_answer):
    reply = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
            {"role": "assistant", "content": user_answer},
            {
                "role": "user",
                "content": "Si ma réponse est correcte, félicites moi; sinon dis que c'est faux et donnes moi la bonne réponse",
            },
        ],
    )
    return reply["choices"][0]["message"]["content"]
