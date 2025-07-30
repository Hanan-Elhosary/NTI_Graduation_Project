from crewai import Task
from agents.conversational_agent import conversational_agent
from agents.dashboard_agent import dashboard_agent

conversational_data_analysis = Task(
    description="Analyze user queries related to complaints and provide insights.",
    expected_output="Actionable insights or user response",
    agent=conversational_agent
)

dashboard_visualization_task = Task(
    description="Generate an interactive dashboard from the provided complaints dataset.",
    expected_output="A rendered dashboard",
    agent=dashboard_agent
)
