from valor.assistant import Assistant
from valor.tools.duckduckgo import DuckDuckGo
from valor.tools.website import WebsiteTools
from valor.llm.ollama import Hermes

assistant = Assistant(
    llm=Hermes(model="adrienbrault/nous-hermes2pro:Q8_0"), tools=[DuckDuckGo(), WebsiteTools()], show_tool_calls=True
)
assistant.print_response(
    "Produce a report about NousResearch. Search for their website and huggingface. Read both urls and provide a detailed summary along with a unique fact. Then draft a message to NousResearch thanking them for their amazing work.",
    markdown=True,
)
