from crewai import Crew
from tasks import conversational_data_analysis, dashboard_visualization_task
import os
from utils import get_openai_api_key

os.environ["OPENAI_API_KEY"] = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"

crew = Crew(
    tasks=[
        conversational_data_analysis,
        dashboard_visualization_task
    ],
    verbose=True
)

if __name__ == "__main__":
    user_input = input("Enter your query: ")
    result = crew.run({
        "argument": user_input,
        "csv_path": "data/your_csv_file.csv"
    })
    print(result)