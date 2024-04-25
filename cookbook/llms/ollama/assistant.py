from valor.assistant import Assistant
from valor.llm.ollama import Ollama

assistant = Assistant(
    llm=Ollama(model="openhermes"),
    description="You help people with their health and fitness goals.",
)
assistant.print_response("Share a quick healthy breakfast recipe.", markdown=True)
