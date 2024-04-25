from valor.assistant import Assistant
from valor.llm.anyscale import Anyscale

assistant = Assistant(llm=Anyscale(model="mistralai/Mixtral-8x7B-Instruct-v0.1"))
assistant.cli_app(markdown=True)
