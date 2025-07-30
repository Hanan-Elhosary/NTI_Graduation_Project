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
