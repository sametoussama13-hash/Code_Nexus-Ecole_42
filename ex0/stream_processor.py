#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    """Class data."""

    def __init__(self) -> None:
        """Init class Dataprocessor"""
        pass

    @abstractmethod
    def process(self, data: Any) -> str:
        """Process data."""
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Chack data."""
        pass

    @abstractmethod
    def format_output(self, result: str) -> str:
        "print result"
        pass


class NumericProcessor(DataProcessor):
    """Class NumericProcessor."""

    def __init__(self) -> None:
        "Init NumericProcessor."
        super().__init__()
        self.len_num: int = 0
        self.sum_data: int = 0
        self.avg_data: Any = None

    def process(self, data: Any) -> str:
        "Prcess NumericProcessor"
        data_p = str(data).split()
        num = [int(x) for x in data_p]
        self.len_num = len(data_p)
        self.sum_data = sum(num)
        self.avg_data = (self.sum_data / self.len_num)
        return (
            f"Processed {self.len_num} numeric values,"
            f" sum={self.sum_data}, avg={self.avg_data}"
        )

    def validate(self, data: Any) -> bool:
        """Valid is Numeric"""
        valid: str = "".join(str(data).split('-'))
        valid = "".join(str(valid).split())
        if valid.isdigit():
            print("Initializing Numeric Processor...")
            print(f"Processing data: {str(data).split()}")
            print("Validation: Numeric data verified")
            return True
        return False

    def format_output(self, result: str) -> str:
        "Put the result."
        return result


class TextProcessor(DataProcessor):
    """Class Text Processor."""

    def __init__(self) -> None:
        "init Text Processor."
        super().__init__()
        self.len_data: int = 0
        self.len_word: int = 0

    def process(self, data: Any) -> str:
        "Process Text Processor."
        data = str(data)
        self.len_data = len("".join(data.split()))
        self.len_word = len(data.split())
        return (
            f"Processed text: {self.len_data} characters,"
            f" {self.len_word} words"
        )

    def validate(self, data: Any) -> bool:
        """Valid is alpha."""
        if "".join(str(data).split()).isalpha():
            print("Initializing Text Processor...")
            print(f"Processing data: {data}")
            print("Validation: Text data verified")
            return True
        return False

    def format_output(self, result: str) -> str:
        "Put the result."
        return result


class LogProcessor(DataProcessor):
    """Class Log Processor."""

    def __init__(self) -> None:
        "Init Log Processor."
        super().__init__()
        self.log: Any = None

    def process(self, data: Any) -> str:
        "Process Log Processor."
        data = str(data)
        if "ALERT" in data or "ERROR" in data:
            self.log = "".join(str(data).split(":", -1))
        elif "INFO" in data:
            self.log = "".join(str(data).split(":", -1))
        return (
            f"[ALERT] {self.log.split(' ')[0]} level detected:"
            f" {self.log.split(' ', 1)[1]}"
        )

    def validate(self, data: Any) -> bool:
        """Valid is log."""
        if "ERROR" in data or "ALERT" in data:
            print("Initializing Log Processor...")
            print(f"Processing data: {data}")
            print("Validation: Log entry verified")
            return True
        return False

    def format_output(self, result: str) -> str:
        "Put the result."
        return result


def stream_processor(data: Any) -> None:
    """Stream prcessor."""
    info: list[str] = []
    processors = (
        NumericProcessor(),
        TextProcessor(),
        LogProcessor()
    )
    print("\n=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")
    try:
        for d in data:
            for p in processors:
                if p.validate(d):
                    result = p.process(d)
                    info.append(result)
                    print(f"Output: {p.format_output(result)}\n")
        print("\n=== Polymorphic Processing Demo ===")
        i: int = 1
        for n in info:
            print(f"result {i}: {n}")
            i += 1
    except Exception as e:
        print(e)
    finally:
        print(
            "\nFoundation systems online."
            "Nexus ready for advanced streams.\n"
        )


if __name__ == "__main__":
    data: list[str] = ["-12 3 -4 56 78", "abcd",  "ERROR: Connection timeout"]
    stream_processor(data)
