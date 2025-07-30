from crewai import Task
from agents.conversational_agent import conversational_agent

conversational_data_analysis = Task(
    description="Analyze and respond to user's data-related questions in natural language.",
    expected_output="Clear, human-friendly answer based on the dataset.",
    agent=conversational_agent,
)

# dashboard tasks
from crewai import Task
from agents.dashboard_agent import dashboard_agent

dashboard_visualization_task = Task(
    description="Generate a full dashboard based on complaint dataset with charts and trends.",
    expected_output="HTML output with embedded charts (WordCloud, bar charts, line charts)",
    agent=dashboard_agent,
)
