import typer
from typing import Sequence, Union, List, Optional
from distortme.nn_algorithms.utils.base_wrapper import BaseWrapper
from distortme.base_types import Image, BaseResult


class NetworkContext:
    def __init__(self, tag: str = "Default context") -> None:
        self.tag = tag
        self._model: Optional[BaseWrapper] = None

    def __repr__(self):
        return f"Context: [{self.tag}]\nmodel: [{self._model}]"

    @property
    def model(self) -> Optional[BaseWrapper]:
        return self._model

    @model.setter
    def model(self, new_model: BaseWrapper) -> None:
        typer.echo(f"Loading [{new_model}]")
        self._model = new_model
        status = self._model.load()
        if status:
            typer.echo("Status: [Done]")
        else:
            typer.echo("Status: [Fail]")
            typer.Exit()

    @model.getter
    def model(self) -> Optional[BaseWrapper]:
        return self._model

    def predict(self, image: Union[Image, Sequence[Image]]) -> List[BaseResult]:
        if self._model is not None:
            return self._model.predict(image)
        else:
            print("Model was not assigned to context")
            exit(-1)
