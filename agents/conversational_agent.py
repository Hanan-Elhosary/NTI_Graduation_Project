from crewai import Agent
from tools.conversational_tool import ConversationalTool
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    max_tokens=100
)

conversational_agent = Agent(
    role="Conversational AI Agent",
    goal="Understand and respond to user questions; delegate analysis to dashboard agent.",
    backstory="You engage users in natural conversations and know when to pass to analytics.",
    tools=[ConversationalTool()],
    llm=llm,
    allow_delegation=True,
    verbose=True
)