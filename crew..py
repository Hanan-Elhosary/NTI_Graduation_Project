# run_crew.py
from crewai import Crew
from tasks import conversational_data_analysis, dashboard_visualization_task

# Create Crew
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
        "csv_path": "data/your_csv_file.csv"  # عدل الاسم حسب الملف
    })
    print(result)
