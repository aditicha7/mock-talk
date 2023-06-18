import os
import openai

API_KEY = "INSERT API KEY HERE"

openai.api_key = API_KEY

deadline = input(
    "Welcome to MockTalk.ai! We're here to help you prepare for any upcoming interviews that you may have. \n"
    "To start off, when is the date of your interview (MM/DD/YYYY)? \n")
company = input("What is the company you are applying to: ")
role = input("What is the role that you wish to apply as: ")
difficulty = input("What is the experience level of the position: ")

interview_question = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Do not include both at the same time. Provide either a {difficulty} interview question or a leetcode prompt. You are an interviewing me who wants to work at {company} as a {difficulty} {role}.",
    temperature=1,
    max_tokens=150,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
)

answer = input(interview_question["choices"][0]["text"])

while True:
    question = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"How good was my response for an interview setting?\n"
               f"Ask a follow up interview question.",
        temperature=1,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    next_answer = input(question["choices"][0]["text"])

    end = input("Are you done with answering questions for now? ")
    if end == "yes":
        break

    else:
        question = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Ask a follow up interview question.",
            temperature=1,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        next_answer = input(question["choices"][0]["text"])
