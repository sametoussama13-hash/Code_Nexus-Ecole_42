#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Any, Optional, Union


class DataStream(ABC):
    """Class Data Stream."""

    def __init__(self, stream_id: str, stream_type: str) -> None:
        """Init Data Stream."""
        self.stream_id = stream_id
        self.stream_type = stream_type 

    @abstractmethod
    def process_batch(self, data_batch: list[Any]) -> str:
        """Process data."""
        pass

    def filter_data(self, data_batch: list[Any], critera: Optional[Any]) -> list[Any]:
        """Filter data."""
        pass

    def get_stats(self) -> dict[str, Union[str, int, float]]:
        """Get stats."""
        pass


class SensorStream(DataStream):
    """Class Sensor Stream."""

    def __init__(self, stream_id: str, stream_type: str) -> None:
        """Init Sensor stream."""
        super().__init__(stream_id, stream_type)

    def process_batch(self, data_batch: list[Any]) -> None:
        """Process data."""
        print(f"Stream ID: {self.stream_id}, Type: {self.stream_type}")

    # {'temp': 22.5, 'humidity': 65, 'pressure': 1013}

class TransactionStream(DataStream):
    """Class Transaction Stream."""

    def __init__(self, stream_id: str, stream_type: str) -> None:
        """Init Transaction Stream."""
        super().__init__(stream_id, stream_type)
        self.temp = 0
        self.humidity = 0
        self.pressur = 0

    def process_batch(self, data_batch: list[Any]) -> str:
        """Process data."""
        print(f"Stream ID: {self.stream_id}, Type: {self.stream_type}")
        print(f"Processing sensor batch: {data_batch}")
        data: list[float] = []
        i: int = 0
        for v in data_batch:
            v = str(v).split(":", 1)[1]
            data.append(v)
        for s in data and i < 3:
            if i == 0:
                self.temp = float(s)
            elif i == 1:
                self.humidity = float(s)
            else:
                self.pressur = float(s)
            i += 1
        return f"{i} readings processed, avg temp: {}"

    
class EventStream(DataStream):
    """Class Event Stream."""

    def __init__(self, stream_id: str, stream_type: str) -> None:
        """Init Event Stream."""
        super().__init__(stream_id, stream_type)

    def process_batch(self, data_batch: list[Any]) -> str:
        """Process data."""
        print(f"Stream ID: {self.stream_id}, Type: {self.stream_type}")


class StreamProcessor:
    """Class stream processor."""

    data_list: list[Any] = []

    @staticmethod
    def add_data(data: Any) -> None:
        """Add data."""
        StreamProcessor.data_list.append(data)
    

def data_stream(data_batch: Any) -> None:
    """Stream data."""
    print("\n=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")
    sensor_keys: list[str] = ["temp", "humidity", "pressure"]
    trans_keys: list[str] = ["buy", "sell", "buy"]
    event_keys: list[str] = ["login", "error", "logout"]
    sensor: int = 1
    trans: int = 1
    event: int = 1
    try:
        for d in data_batch:
            data: list = []
            if all(":" in s for s in d):
                check = ":".join(d).split(":")
                if any(k in check for k in sensor_keys):
                    print("\nInitializing Sensor Stream...")
                    if not (f for f in data if isinstance(f, float)):
                        raise Exception(
                            "TypeError: the Type of valeu Sensor data not int"
                        )
                    if len(data) < 3:
                        raise Exception(
                            "TypeError: the Type of valeu Sensor data not int"
                        )
                    r = SensorStream(f"SENSOR_{str(sensor)}",
                                     "Environmental Data")
                    r.process_batch(data)
                    StreamProcessor.add_data(r)
                    sensor += 1
                elif any(k in check for k in trans_keys):
                    print("\nInitializing Transaction Stream...")
                    for v in d:
                        v = str(v).split(":", 1)[1]
                        data.append(v)
                    if not (f for f in data if isinstance(f, int)):
                        raise Exception(
                            "TypeError: the Type of valeu Sensor data not int"
                        )
                    if len(data) < 3:
                        raise Exception(
                            f"Miss data: you send {len(data)}"
                            " valeus you need 3"
                        )
                    r = TransactionStream(f"TRANS_{str(trans)}",
                                          "Financial Data")
                    r.process_batch(data)
                    trans += 1
            else:
                print("\nInitializing Event Stream...")
                if any(k in d for k in event_keys):
                    if not (f for f in data if isinstance(f, str)):
                        raise Exception(
                            "TypeError: the Event Stream need str data"
                        )
                    r = EventStream(f"EVENT_{str(event)}", "System Events")
                    r.process_batch(d)
                    event += 1
    except Exception as e:
        print(e)


if __name__ == "__main__":
    data_batch: list[Any] = [
        ["temp:22.5", "humidity:65", "pressure:1013"],
        ["buy:100", "sell:150", "credit:75"],
        ["login", "error", "logout"]
    ]
    data_stream(data_batch)

