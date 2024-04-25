from typing import List
from pydantic import BaseModel, Field
from rich.pretty import pprint
from valor.assistant import Assistant
from valor.llm.ollama import Ollama


class MovieScript(BaseModel):
    setting: str = Field(..., description="Provide a nice setting for a blockbuster movie.")
    ending: str = Field(..., description="Ending of the movie. If not available, provide a happy ending.")
    genre: str = Field(
        ..., description="Genre of the movie. If not available, select action, thriller or romantic comedy."
    )
    name: str = Field(..., description="Give a name to this movie")
    characters: List[str] = Field(..., description="Name of characters for this movie.")
    storyline: str = Field(..., description="3 sentence storyline for the movie. Make it exciting!")


movie_assistant = Assistant(
    llm=Ollama(model="openhermes"),
    description="You help people write movie ideas.",
    output_model=MovieScript,
    # debug_mode=True,
)

pprint(movie_assistant.run("New York"))
