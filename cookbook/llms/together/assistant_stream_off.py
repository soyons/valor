from valor.assistant import Assistant
from valor.llm.together import Together

assistant = Assistant(
    llm=Together(model="mistralai/Mixtral-8x7B-Instruct-v0.1"),
    description="You help people with their health and fitness goals.",
)
assistant.print_response("Share a quick healthy breakfast recipe.", markdown=True, stream=False)
