from crewai import Agent
from tools.dashboard_tool import DashboardTool
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    max_tokens=100
)

dashboard_agent = Agent(
    role="Consumer Complaints Dashboard Agent",
    goal="Generate dashboards from complaint datasets",
    backstory="You are a Data Analytics Agent skilled in generating insights from complaint data.",
    tools=[DashboardTool()],
    llm=llm,  # تمرير الموديل هنا
    allow_delegation=False,
    verbose=True
)