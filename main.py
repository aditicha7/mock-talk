import os
import openai

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
        prompt=f"How good was my response ({answer}) for an interview setting? How can I improve on my response?",
        temperature=1,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    input(question["choices"][0]["text"])

    end = input("Are you done with answering questions for now? ")
    if end.lower() == "yes":
        print("/nThank you for trying MockTalk :) See you next time!")
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

        answer = input(question["choices"][0]["text"])


answer = input(question["choices"][0]["text"])

print(response["choices"][0]["text"])
#roles, type of coding, companies,