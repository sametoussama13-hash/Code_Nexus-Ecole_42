#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Any

class DataStream(ABC):
    """Class Data Stream."""

    def __init__(self) -> None:
        """Init Data Stream."""


class SensorStream(DataStream):
    """Class Sensor Stream."""

    def __init__(self) -> None:
        """Init Sensor stream."""
        super().__init__()


def data_stream() -> None:
    



if __name__ == "__main__":
    data_stream()
