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
        pass

    @abstractmethod
    def process(self, data: Any) -> Union[str, Any]:
        """Process data."""
        pass


class JSONAdapter(ProcessingPipline):
    """Init JSON Adapter."""

    def __init__(self, pipline_id: str) -> None:
        """Init JSON Adapter."""
        self.pipline_id = pipline_id

    def process(self, data: Any) -> Union[str, Any]:
        """Process data."""


class CSVAdapter(ProcessingPipline):
    """Init CSV Adapter."""

    def __init__(self, pipline_id: str) -> None:
        """Init JSON Adapter."""
        self.pipline_id = pipline_id

    def process(self, data: Any) -> Union[str, Any]:
        """Process data."""


class StreamAdapter(ProcessingPipline):
    """Class Stream adapter"""

    def __init__(self, pipline_id: str) -> None:
        """Init JSON Adapter."""
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
        

class TransfomStage:
    """Class Transfom Stage."""

    def process(self, data: Any) -> Any:
        """Process data."""

class OutputStage:
    """Class Output Stage."""

    def process(self, data: Any) -> Any:
        """Process data."""

class NexusManager:
    """Class Nexus Manager."""

    def __init__(self) -> None:
        """Init Nexus Manager."""

    def handle(self, data: Any) -> Union[str, Any]:
        """Handle Nexus Process."""
        if isinstance(data, dict[Any]):
            jason = JSONAdapter(data)


def nexus_pipeline(data: list[Any]) -> None:
    """Process pipline."""
    nexus = NexusManager()
    for d in data:
        result = nexus.handle(d)


if __name__ == "__main__":
    data: list[Any] = [
        {"sensor": "temp", "value": 23.5, "unit": "C"},
        "user,action,timestamp",
        "Real-time sensor stream"
    ]
    nexus_pipeline(data)
