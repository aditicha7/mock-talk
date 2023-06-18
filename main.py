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

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import SerpAPIWrapper

import os

#environmental variable
API_KEY = "INSERT API KEY HERE"
os.environ["OPENAI_API_KEY"] = API_KEY
os.environ["SERPAPI_API_KEY"] = "INSERT API KEY HERE"

chat = ChatOpenAI(temperature = 0.9, model = "gpt-3.5-turbo-0613")
llm = ChatOpenAI(openai_api_key = "INSERT API KEY HERE")
llm = ChatOpenAI(temperature = 0.9, model = "gpt-3.5-turbo-0613")

template = ("You are an interview chatbot giving job seekers advice for an interview with {company} as {difficulty} {role} by {deadline}, by giving feedback and providing leet code or interview questions. ")
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

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are an interview chatbot giving job seekers advice for an interview with {company} as {difficulty} {role} by {deadline}, by giving feedback and providing leet code or interview questions. "
    ),
    MessagesPlaceholder(variable_name= ""),
    HumanMessagePromptTemplate.from_template("{input}")
])

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
    Tool(
        name = "Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world"
    ),
]
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent = initialize_agent(tools, chat, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

chain.run(
    text = "text",
    deadline = deadline,
    company = company,
    role = role,
    difficulty=difficulty,
    prompt=f"Provide either a interview question based on {role} for a leetcode prompt based on {difficulty} and {role}. You are an interviewing me who wants to work at {company} as a {difficulty} {role}. Do not include both at the same time.",
)

agent.run(f"Provide either a interview question based on {role} for a leetcode prompt based on {difficulty} and {role}. You are an interviewing me who wants to work at {company} as a {difficulty} {role}. Do not include both at the same time.")
agent_chain.run(input="answer")

#everything below is the blueprint

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


answer = input(question["choices"][0]["text"])

print(response["choices"][0]["text"])
#roles, type of coding, companies,