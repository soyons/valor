from valor.assistant import Assistant
from valor.tools.duckduckgo import DuckDuckGo

assistant = Assistant(tools=[DuckDuckGo()], show_tool_calls=True)
assistant.print_response("Whats happening in France?", markdown=True)
