from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, load_tools, Tool

#chat model imports
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
#template imports
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

#for the agent
from langchain import (
    LLMMathChain,
    OpenAI,
    SerpAPIWrapper,
    SQLDatabase,
    SQLDatabaseChain,
)

import os

#environmental variable
API_KEY = "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"
os.environ["OPENAI_API_KEY"] = API_KEY
os.environ["SERPAPI_API_KEY"] = "fcd27d3d2165e05a55c72e78206a097520eecee7c651fd3e5d88d3ef6b5992ce"

chat = ChatOpenAI(temperature = 0.9)
llm = OpenAI(openai_api_key = "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")
llm = OpenAI(temperature = 0.9, model = "text-davinci-003")
#gpt-3.5-turbo-0613

load_tools(["serpapi", "llm-math"], llm=llm)
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
search = SerpAPIWrapper()
db = SQLDatabase.from_uri("sqlite:///chinook.db")
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions",
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math",
    ),
    Tool(
        name="FooBar-DB",
        func=db_chain.run,
        description="useful for when you need to answer questions about FooBar. Input should be in the form of a question containing full context",
    ),
]
agent = initialize_agent(tools, chat, agent=AgentType.OPENAI_FUNCTIONS)

template = "You are an interview chatbot giving job seekers advice for an interview with {company} as {difficulty} {role} by {deadline}, by giving feedback and providing leet code or interview questions. "
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
#chat_prompt.format_messages(text = print("Welcome to MockTalk.ai! We're here to help you prepare for any upcoming interviews that you may have. \nTo start off:\n"), deadline = input("When is the date of your interview (MM/DD/YYYY)?"), company = input("What is the company you are applying to: "), role = input("What is the role that you wish to apply as: "), difficulty = input("What is the experience level of the position: "))

chain = LLMChain(llm = chat, prompt = chat_prompt)
deadline = input("Welcome to MockTalk.ai! We're here to help you prepare for any upcoming interviews that you may have. \nTo start off:\nWhen is the date of your interview (MM/DD/YYYY)? "),
company = input("What is the company you are applying to: ")
role = input("What is the role that you wish to apply as: ")
difficulty = input("What is the experience level of the position: ")

chain.run(
    text = 'text',
    deadline = deadline,
    company = company,
    role = role,
    difficulty=difficulty,
    prompt=f"Provide either a interview question based on {role} for a leetcode prompt based on {difficulty} and {role}. You are an interviewing me who wants to work at {company} as a {difficulty} {role}. Do not include both at the same time."
)


#"Then, you give feedback after their answer, and ask if they want to continue. Depending on their answer, you either stop the code when the user says no, or repeat this prompt when the user wants to continue."

# interview_question = OpenAI.Completion.create(
#     model="text-davinci-003",
#     prompt=f"Do not include both at the same time. Provide either a {difficulty} interview question or a leetcode prompt. You are an interviewing me who wants to work at {company} as a {difficulty} {role}.",
#     temperature=1,
#     max_tokens=150,
#     top_p=1.0,
#     frequency_penalty=0.0,
#     presence_penalty=0.0
# )
#
# answer = input(interview_question["choices"][0]["text"])
#
# while True:
#     question = OpenAI.Completion.create(
#         model="text-davinci-003",
#         prompt=f"How good was my response ({answer}) for an interview setting? How can I improve on my response?",
#         temperature=1,
#         max_tokens=150,
#         top_p=1.0,
#         frequency_penalty=0.0,
#         presence_penalty=0.0
#     )
#
#     input(question["choices"][0]["text"])
#
#     end = input("Are you done with answering questions for now? ")
#     if end.lower() == "yes":
#         print("/nThank you for trying MockTalk :) See you next time!")
#         break
#
#     else:
#         question = OpenAI.Completion.create(
#             model="text-davinci-003",
#             prompt=f"Ask a follow up interview question.",
#             temperature=1,
#             max_tokens=150,
#             top_p=1.0,
#             frequency_penalty=0.0,
#             presence_penalty=0.0
#         )
#
#         answer = input(question["choices"][0]["text"])

