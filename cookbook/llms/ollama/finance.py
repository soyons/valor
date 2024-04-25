from valor.assistant import Assistant
from valor.tools.yfinance import YFinanceTools
from valor.llm.ollama import OllamaTools

print("============= llama3 finance assistant =============")
assistant = Assistant(
    llm=OllamaTools(model="llama3"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)],
    show_tool_calls=True,
)
assistant.cli_app(markdown=True)
