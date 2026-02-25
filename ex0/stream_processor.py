#!/usr/bin/env python3
from abc import ABC, abstractmethod
import Any

class DataProcessor:
    """Class data."""

    def __init__(self, data: list) -> None:
        """Init class Dataprocessor"""
        self.data = data

    @abstractmethod
    def process(self, data: list) -> str:
        """Process data."""
        pass

    @abstractmethod
    def validation(self, data: list) -> bool:
        """Chack data."""
        pass

class NumericProcessor(DataProcessor):
    """Class NumericProcessor."""

    def __init__(self, data: Any) -> None:
        super().__init__(data)

    def process(self, data) -> str:

    def validation(self, data) -> bool:
        """Valid is Numeric"""
        if isinstance(data, (int, float)):
            return True
        return False

    def format_output(self, data) -> str:


class TextProcessor(DataProcessor):
    """Class NumericProcessor."""

    def __init__(self, data: list) -> None:
        super().__init__(data)
        self.data: list = []

    def process(self, data) -> str:
        len_data: int = len("".join(data.split()))
        len_word: int = len(data.split())
        return self.data.append(data, len_data, len_word)

    def validation(self, data) -> bool:
        """Valid is alpha."""
        if "".join(data.split()).isalpha():
            return True
        return False

    def format_output(self, data) -> str:


class LogProcessor(DataProcessor):
    """Class NumericProcessor."""

    def __init__(self, data: list) -> None:
        super().__init__(data)
        self.data = process(data)

    def process(self, data) -> str:
        return

    def validation(self, data) -> bool:
        """Valid is log."""
        if "ERROR" or "ALERT" in data:
            return True
        return False 

    def format_output(self, data) -> str:


def stream_processor() -> None:
    """Stream prcessor."""
    DataProcessor = (NumericProcessor(), TextProcessor(), LogProcessor())
    data: list = ["12345678", "abcd",  "ERROR: Connection timeout"]
    for l in data:
        for p in DataProcessor:
            if p.validation(l):
                p.process(data)



if __name__ == "__main__":
    stream_processor()