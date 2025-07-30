from crewai import Agent
from tools.conversational_tool import ConversationalTool

conversational_agent = Agent(
    role="Conversational AI Agent",
    goal="Understand and respond to user questions; delegate analysis to dashboard agent.",
    backstory="You engage users in natural conversations and know when to pass to analytics.",
    tools=[ConversationalTool()],
    allow_delegation=True,
    verbose=True
)

#dashboard
from crewai import Agent
from tools.dashboard_tool import DashboardTool

dashboard_agent = Agent(
    role="Consumer Complaints Dashboard Agent",
    goal="Generate dashboards from complaint datasets",
    backstory="You are a Data Analytics Agent skilled in generating insights from complaint data.",
    tools=[DashboardTool()],
    allow_delegation=False,
    verbose=True
)
