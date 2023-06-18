# from flask import Flask
#
# app = Flask(__name__)
#
# @app.route('/')
# def hello():
#     return 'Hello, Flask!'
#
# @app.route('/<username>')
# def bro(username):
#     return f"Hello there, {username}!"
#
# @app.route('/')
# def home():
#     return render_template('index.html')
#
# @app.route('/interview', methods=['GET', 'POST'])
# # def interview():
# #     if request.method == 'POST':
# #         # Handle form submission
# #         name = request.form['name']
# #         # Process the form data and perform any necessary actions
# #         # For example, you could pass the user's name to your AI model to generate interview questions
# #         return render_template('interview.html', name=name)
# #     else:
# #         return render_template('interview.html')
#
# if __name__ == '__main__':
#     app.run(debug=True)

import os
import openai
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = "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"
openai.api_key = API_KEY

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/interview', methods=['POST'])
def interview():
    # deadline = request.form.get('deadline')
    company = request.form.get('company')
    role = request.form.get('role')
    difficulty = request.form.get('difficulty')

    interview_question = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Do not include both at the same time. Provide either a {difficulty} interview question or a leetcode prompt. You are an interviewing me who wants to work at {company} as a {difficulty} {role}.",
        temperature=1,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    answer = interview_question["choices"][0]["text"]

    return render_template('interview.html', answer=answer)

@app.route('/<username>')
def usernum(username):
    return f"Hello {username}"

@app.route('/feedback', methods=['POST'])
def feedback():
    answer = request.form.get('answer')

    question = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"How good was my response ({answer}) for an interview setting? How can I improve on my response?",
        temperature=1,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    return question["choices"][0]["text"]

@app.route('/follow-up', methods=['POST'])
def follow_up():
    answer = request.form.get('answer')

    question = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Ask a follow-up interview question.",
        temperature=1,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    answer = question["choices"][0]["text"]

    return render_template('interview.html', answer=answer)

if __name__ == '__main__':
    app.run()


