from valor.assistant import Assistant
from valor.tools.duckduckgo import DuckDuckGo

assistant = Assistant(tools=[DuckDuckGo()], show_tool_calls=True, read_chat_history=True)
assistant.cli_app(markdown=True)
