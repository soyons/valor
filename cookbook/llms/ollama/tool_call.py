import typer
from valor.assistant import Assistant
from valor.tools.duckduckgo import DuckDuckGo
from valor.llm.ollama import OllamaTools


def tool_call(model: str = "openhermes", debug: bool = False):
    print(f"============= Running: {model} =============")
    Assistant(
        llm=OllamaTools(model=model),
        tools=[DuckDuckGo()],
        show_tool_calls=True,
        debug_mode=debug,
    ).cli_app(markdown=True)


if __name__ == "__main__":
    typer.run(tool_call)
