import torch
import openai
import sqlite3
import pymorphy2

from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer


openai.api_key = "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"

engine = "text-davinci-003"


def faind_ans_rezerv(text):
    morph = pymorphy2.MorphAnalyzer()
    con = sqlite3.connect('DBs\znach.sqlite')
    cur = con.cursor()
    s = text.split()
    res = []
    for i in s:
        p = morph.parse(i)[0]
        res.append((i.lower(), p.normal_form))
    itogo = []
    for i in res:
        a = i[1]
        znach = cur.execute(f"""Select zn from data WHERE Word='{a}'""").fetchall()
        if znach != []:
            itogo.append(f'{a} - {znach[0][0]}')
    cur.close()
    return '\n'.join(itogo)

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
    return faind_ans_rezerv(text)


if __name__ == '__main__':
    app.run()