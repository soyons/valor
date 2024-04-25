from valor.assistant import Assistant
from valor.llm.ollama import Ollama
from valor.tools.duckduckgo import DuckDuckGo

hermes = Assistant(
    llm=Ollama(model="openhermes"),
    tools=[DuckDuckGo()],
    show_tool_calls=True,
)
hermes.print_response("Whats happening in France? Summarize top stories with sources.", markdown=True)
