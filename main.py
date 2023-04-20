import torch
import openai

from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer


openai.api_key = "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"

engine = "text-davinci-003"

def find_ans(text):
    # Запрос
    prompt = f"Раскажи что значит мой сон:\n{text}"

    # Модель
    completion = openai.Completion.create(engine=engine,
                                          prompt=prompt,
                                          temperature=0.4,
                                          max_tokens=1000)

    return completion.choices[0]['text'].split('\n')[-1]

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('both.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return get_Chat_response(input)


def get_Chat_response(text):
    return find_ans(text)


if __name__ == '__main__':
    app.run()