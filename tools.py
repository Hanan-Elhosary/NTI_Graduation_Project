from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class ConversationalToolInput(BaseModel):
    argument: str = Field(..., description="The user message to process and respond to")

class ConversationalTool(BaseTool):
    name: str = "Conversational Tool"
    description: str = "Handles general or conversational questions"
    args_schema: Type[BaseModel] = ConversationalToolInput

    def _run(self, argument: str) -> str:
        lowered = argument.lower()
        if "chart" in lowered or "visualize" in lowered or "dashboard" in lowered:
            return (
                "This seems like a request for data visualization or dashboard interaction. "
                "Please forward it to the dashboard agent."
            )
        return f"Sure! Here's a response to your message: '{argument}'"

#dashboard tools
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for image generation

class DashboardToolInput(BaseModel):
    csv_path: str = Field(..., description="Path to the CSV file containing complaint data")

class DashboardTool(BaseTool):
    name: str = "Dashboard Tool"
    description: str = (
        "Analyzes complaint data and generates charts like word frequency, "
        "product categories, company complaints, state-wise distribution, and complaints over time."
    )
    args_schema: Type[BaseModel] = DashboardToolInput

    def _run(self, csv_path: str) -> str:
        try:
            df = pd.read_csv(csv_path)

            images_html = []

            # Word Cloud
            text_data = ' '.join(df.select_dtypes(include='object').astype(str).stack().tolist())
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
            images_html.append(self._save_plot_image(wordcloud.to_image(), "Word Frequency Cloud"))

            # Bar Chart: Complaints by Product
            if 'Product' in df.columns:
                images_html.append(self._plot_bar(df['Product'], "Complaints by Product"))

            # Bar Chart: Complaints by Company
            if 'Company' in df.columns:
                images_html.append(self._plot_bar(df['Company'], "Complaints by Company"))

            # Bar Chart: Complaints by State
            if 'State' in df.columns:
                images_html.append(self._plot_bar(df['State'], "Complaints by State"))

            # Line Chart: Complaints over Time
            if 'Date received' in df.columns:
                df['Date received'] = pd.to_datetime(df['Date received'], errors='coerce')
                time_series = df['Date received'].dt.to_period('M').value_counts().sort_index()
                fig, ax = plt.subplots(figsize=(10, 4))
                time_series.plot(ax=ax)
                ax.set_title("Complaints Over Time")
                ax.set_xlabel("Month")
                ax.set_ylabel("Number of Complaints")
                images_html.append(self._save_plot_image(fig))

            return "<br><br>".join(images_html)

        except Exception as e:
            return f"Error while generating dashboard: {e}"

    def _plot_bar(self, series, title):
        fig, ax = plt.subplots(figsize=(10, 4))
        series.value_counts().head(10).plot(kind='bar', ax=ax)
        ax.set_title(title)
        ax.set_ylabel("Count")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        return self._save_plot_image(fig, title)

    def _save_plot_image(self, image_or_fig, alt_text="Chart"):
        buf = io.BytesIO()
        if hasattr(image_or_fig, "savefig"):  # it's a matplotlib fig
            image_or_fig.savefig(buf, format='png', bbox_inches='tight')
        else:  # it's a PIL image (like wordcloud)
            image_or_fig.save(buf, format='png')
        base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
        return f"<h4>{alt_text}</h4><img src='data:image/png;base64,{base64_img}'/>"