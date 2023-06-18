import os
import openai
import time

API_KEY = "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"

openai.api_key = API_KEY

deadline = input(
    "Welcome to MockTalk.ai! We're here to help you prepare for any upcoming interviews that you may have. \n"
    "To start off, when is the date of your interview (MM/DD/YYYY)? \n")
company = input("What is the company you are applying to: ")
role = input("What is the role that you wish to apply as: ")
difficulty = input("What is the experience level of the position: ")

interview_question = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Do not include both at the same time. You are an interviewing someone who wants to work at {company} as a {difficulty} {role}. "
           f"Provide either a {difficulty} interview question or a leetcode prompt.",
    temperature=1,
    max_tokens=150,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
)

answer = input(interview_question["choices"][0]["text"])

question = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Based on {company}'s core values, how good was their response?\n"
           f"Ask a follow up interview question.",
    temperature=1,
    max_tokens=150,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
)

next_answer = input(question["choices"][0]["text"])
