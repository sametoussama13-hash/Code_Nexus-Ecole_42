#!/usr/bin/env python3
from typing import Any, Optional, Protocol, Union
from abc import ABC, abstractmethod
from collections import deque, Counter, defaultdict, namedtuple, ChainMap

""" 'deque((maxlen=N))' permet de garder les dernier ellement ajouetr dans une liste."""
""" 'counetr' est un (dict) sert à augmenter la valeur de la clés et la rajouter so elle existe pas."""
""" 'defaultdict' est un (dict) qui permet d'ajouter une cles si elle n'existe pas.""" 
""" 'namedtuple' est un style de tuple qui fonctionne comme instance de class avec des attribut au sein de son tuple. """
""" 'ChainMap' est un dict qui permet de metre plusieur dict de dans et qui cherche les clés par ordre de classement. """
class ProcessingPipline(ABC):
    """Class Processing Pipline."""

    def __init__(self) -> None:
        """Init Processing Pipline."""
        self.normalize: list[dict[str, Any]] = []
        self.stage: tuple[ProcessingStage] = (InputStage(), TransformStage(), OutputStage())

    def add_stage(self, stage) -> None:
        """Add Stage."""
        for stage in self.stage:
            data = stage.process(data)
        return data

    @abstractmethod
    def process(self, data: Any) -> Union[str, Any]:
        """Process data."""
        pass


class JSONAdapter(ProcessingPipline):
    """Init JSON Adapter."""

    def __init__(self, pipline_id: str) -> None:
        """Init JSON Adapter."""
        super().__init__()
        self.pipline_id = pipline_id

    def process(self, data: Any) -> Union[str, Any]:
        """Process data."""
        records = {"source": "JSON", "records": [data]}
        self.normalize.append(records)
        return self.add_stage(records)


class CSVAdapter(ProcessingPipline):
    """Init CSV Adapter."""

    def __init__(self, pipline_id: str) -> None:
        """Init JSON Adapter."""
        super().__init__()
        self.pipline_id = pipline_id

    def process(self, data: Any) -> Union[str, Any]:
        """Process data."""


class StreamAdapter(ProcessingPipline):
    """Class Stream adapter"""

    def __init__(self, pipline_id: str) -> None:
        """Init JSON Adapter."""
        super().__init__()
        self.pipline_id = pipline_id

    def process(self, data: Any) -> Union[str, Any]:
        """Process data."""


class ProcessingStage(Protocol):
    """Init Process Stage."""

    def process(self, data: Any) -> Any:
        """Process data."""
        pass


class InputStage:
    """Class Input Stage."""

    def process(self, data: Any) -> Any:
        """Process data."""
        pass


class TransformStage:
    """Class Transfom Stage."""

    def process(self, data: Any) -> Any:
        """Process data."""
        pass


class OutputStage:
    """Class Output Stage."""

    def process(self, data: Any) -> Any:
        """Process data."""
        pass


class NexusManager:
    """Class Nexus Manager."""

    def __init__(self) -> None:
        """Init Nexus Manager."""
        self.pipline_json = 0
        self.pipline_csv = 0
        self.pipline_stream = 0

    def handle(self, data: Any) -> Union[str, Any]:
        """Handle Nexus Process."""
        input = InputStage()
        input.process(data)
        if isinstance(data, dict):
            self.pipline_json += 1
            json = JSONAdapter(f"JSON {self.pipline_json}")
            data_result: list[Any] = data
            json.process(data_result)
        elif isinstance(data, list):
            csv = CSVAdapter(data)


def nexus_pipeline(data: list[Any]) -> None:
    """Process pipline."""
    nexus = NexusManager()
    try:
        for d in data:
            result = nexus.handle(d)

    except Exception as e:
        print(e)
    print("fin")


if __name__ == "__main__":
    data: list[Any] = [
        {"sensor": "temp", "value": 23.5, "unit": "C"},
        "user,action,timestamp",
        "Real-time sensor stream"
    ]
    nexus_pipeline(data)
