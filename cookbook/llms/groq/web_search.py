from valor.assistant import Assistant
from valor.tools.duckduckgo import DuckDuckGo
from valor.llm.groq import Groq

assistant = Assistant(
    llm=Groq(model="llama3-70b-8192"),
    tools=[DuckDuckGo()],
    instructions=["Always search the web for information"],
    show_tool_calls=True,
)
assistant.cli_app(markdown=True, stream=False)
# assistant.print_response("Whats happening in France?", markdown=True, stream=False)
