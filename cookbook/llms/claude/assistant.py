from valor.assistant import Assistant
from valor.tools.duckduckgo import DuckDuckGo
from valor.llm.anthropic import Claude

assistant = Assistant(
    llm=Claude(model="claude-3-opus-20240229"),
    tools=[DuckDuckGo()],
    show_tool_calls=True,
)
assistant.print_response("Whats happening in France?", markdown=True)
