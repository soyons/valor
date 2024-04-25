from uuid import uuid4
from textwrap import dedent
from typing import List, Any, Optional, Dict, Iterator, Union

from pydantic import BaseModel, ConfigDict, field_validator, Field

from valor.assistant.assistant import Assistant
from valor.tools.function import Function
from valor.utils.log import logger, set_log_level_to_debug
from valor.utils.message import get_text_from_message
from valor.utils.timer import Timer


class Team(BaseModel):
    name: Optional[str] = None

    lead: Optional[Assistant] = None
    assistants: Optional[List[Assistant]] = None
    reviewer: Optional[Assistant] = None

    # -*- Run settings
    # Run UUID (autogenerated if not set)
    run_id: Optional[str] = Field(None, validate_default=True)
    # Run name
    run_name: Optional[str] = None
    # Metadata associated with this run
    run_data: Optional[Dict[str, Any]] = None

    # If markdown=true, add instructions to format the output using markdown
    markdown: bool = False

    # debug_mode=True enables debug logs
    debug_mode: bool = False
    # monitoring=True logs Assistant runs on phidata.com
    monitoring: bool = False

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("debug_mode", mode="before")
    def set_log_level(cls, v: bool) -> bool:
        if v:
            set_log_level_to_debug()
            logger.debug("Debug logs enabled")
        return v

    @field_validator("run_id", mode="before")
    def set_run_id(cls, v: Optional[str]) -> str:
        return v if v is not None else str(uuid4())

    @property
    def streamable(self) -> bool:
        return True

    def assistant_delegation_function(self, assistant: Assistant, index: int) -> Function:
        def _delegate_task_to_assistant(task_description: str) -> str:
            return assistant.run(task_description, stream=False)  # type: ignore

        assistant_name = assistant.name.replace(" ", "_").lower() if assistant.name else f"assistant_{index}"
        delegation_function = Function.from_callable(_delegate_task_to_assistant)
        delegation_function.name = f"delegate_task_to_{assistant_name}"
        delegation_function.description = dedent(
            f"""Use this function to delegate a task to {assistant_name}
        Args:
            task_description (str): A clear and concise description of the task the assistant should achieve.
        Returns:
            str: The result of the delegated task.
        """
        )
        return delegation_function

    @property
    def leader(self) -> Assistant:
        """Returns the team leader"""

        if self.lead:
            return self.lead

        _delegation_functions = []

        _system_prompt = ""
        if self.assistants and len(self.assistants) > 0:
            _system_prompt += "You are the leader of a team of AI Assistants "
            if self.name:
                _system_prompt += f"called '{self.name}'"
        else:
            _system_prompt += "You are an AI Assistant"

        _system_prompt += " and your goal is to respond to the users message in the best way possible. "
        _system_prompt += "This is an important task and must be done correctly.\n\n"

        if self.assistants and len(self.assistants) > 0:
            _system_prompt += (
                "Given a user message you can respond directly or delegate tasks to the following assistants depending on their role "
                "and the tools available to them. "
            )
            _system_prompt += "\n\n<assistants>"
            for assistant_index, assistant in enumerate(self.assistants):
                _system_prompt += f"\nAssistant {assistant_index+1}:\n"
                if assistant.name:
                    _system_prompt += f"Name: {assistant.name}\n"
                if assistant.role:
                    _system_prompt += f"Role: {assistant.role}\n"
                if assistant.tools is not None:
                    _tools = []
                    for _tool in assistant.tools:
                        if callable(_tool):
                            _tools.append(_tool.__name__)
                    _system_prompt += f"Available tools: {', '.join(_tools)}\n"
                _delegation_functions.append(self.assistant_delegation_function(assistant, assistant_index))
            _system_prompt += "</assistants>\n"

        if self.reviewer is None:
            _system_prompt += (
                "You must review the responses from the assistants and re-run tasks if the result is not satisfactory."
            )

        return Assistant(
            system_prompt=_system_prompt,
            tools=_delegation_functions,
        )

    def _run(
        self, message: Optional[Union[List, Dict, str]] = None, stream: bool = True, **kwargs: Any
    ) -> Iterator[str]:
        logger.debug(f"*********** Team Run Start: {self.run_id} ***********")

        # Get the team leader
        leader = self.leader

        # Final LLM response after running all tasks
        run_output = ""

        if stream and leader.streamable:
            for chunk in leader.run(message=message, stream=True, **kwargs):
                run_output += chunk if isinstance(chunk, str) else ""
                yield chunk if isinstance(chunk, str) else ""
            yield "\n\n"
            run_output += "\n\n"
        else:
            try:
                leader_response = leader.run(message=message, stream=False, **kwargs)
                if stream:
                    yield leader_response  # type: ignore
                    yield "\n\n"
                else:
                    run_output += leader_response  # type: ignore
                    run_output += "\n\n"
            except Exception as e:
                logger.debug(f"Failed to convert task response to json: {e}")

        if not stream:
            yield run_output
        logger.debug(f"*********** Team Run End: {self.run_id} ***********")

    def run(
        self, message: Optional[Union[List, Dict, str]] = None, stream: bool = True, **kwargs: Any
    ) -> Union[Iterator[str], str, BaseModel]:
        if stream and self.streamable:
            resp = self._run(message=message, stream=True, **kwargs)
            return resp
        else:
            resp = self._run(message=message, stream=False, **kwargs)
            return next(resp)

    def print_response(
        self,
        message: Optional[Union[List, Dict, str]] = None,
        stream: bool = True,
        markdown: bool = False,
        **kwargs: Any,
    ) -> None:
        from valor.cli.console import console
        from rich.live import Live
        from rich.table import Table
        from rich.status import Status
        from rich.progress import Progress, SpinnerColumn, TextColumn
        from rich.box import ROUNDED
        from rich.markdown import Markdown

        if markdown:
            self.markdown = True

        if stream:
            response = ""
            with Live() as live_log:
                status = Status("Working...", spinner="dots")
                live_log.update(status)
                response_timer = Timer()
                response_timer.start()
                for resp in self.run(message, stream=True, **kwargs):
                    response += resp if isinstance(resp, str) else ""
                    _response = response if not markdown else Markdown(response)

                    table = Table(box=ROUNDED, border_style="blue", show_header=False)
                    if message:
                        table.show_header = True
                        table.add_column("Message")
                        table.add_column(get_text_from_message(message))
                    table.add_row(f"Response\n({response_timer.elapsed:.1f}s)", _response)  # type: ignore
                    live_log.update(table)
                response_timer.stop()
        else:
            response_timer = Timer()
            response_timer.start()
            with Progress(
                SpinnerColumn(spinner_name="dots"), TextColumn("{task.description}"), transient=True
            ) as progress:
                progress.add_task("Working...")
                response = self.run(message, stream=False, **kwargs)  # type: ignore

            response_timer.stop()
            _response = response if not markdown else Markdown(response)

            table = Table(box=ROUNDED, border_style="blue", show_header=False)
            if message:
                table.show_header = True
                table.add_column("Message")
                table.add_column(get_text_from_message(message))
            table.add_row(f"Response\n({response_timer.elapsed:.1f}s)", _response)  # type: ignore
            console.print(table)
