from pathlib import Path
from valor.assistant.python import PythonAssistant
from valor.file.local.csv import CsvFile

python_assistant = PythonAssistant(
    files=[
        CsvFile(
            path="https://phidata-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv",
            description="Contains information about movies from IMDB.",
        )
    ],
    pip_install=True,
    show_tool_calls=True,
    base_dir=Path(__file__).parent.joinpath("scratch"),
)

python_assistant.cli_app(markdown=True)
