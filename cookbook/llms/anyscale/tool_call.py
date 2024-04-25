from valor.assistant import Assistant
from valor.llm.anyscale import Anyscale
from valor.tools.duckduckgo import DuckDuckGo


assistant = Assistant(llm=Anyscale(), tools=[DuckDuckGo()], show_tool_calls=True, debug_mode=True)
assistant.print_response("Whats happening in France? Summarize top stories with sources.", markdown=True)
