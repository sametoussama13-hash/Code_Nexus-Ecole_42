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

    def filter_data(self, data_batch: list[Any],
                    critera: Optional[Any] = None) -> list[Any]:
        """Filter data."""
        return data_batch

    def get_stats(self) -> dict[str, Union[str, int, float]]:
        """Get stats."""
        return {self.stream_id: self.stream_id, "status": "No stats"}


class SensorStream(DataStream):
    """Class Sensor Stream."""

    def __init__(self, stream_id: str, stream_type: str) -> None:
        """Init Sensor stream."""
        super().__init__(stream_id, stream_type)
        self.process = 0
        self.temp: list[float] = []

    def filter_data(self, data_batch: list[Any],
                    criteria: Optional[Any] = None) -> list[Any]:
        """Filtre data."""
        if criteria == "high":
            data1: list[Any] = []
            for v in data_batch:
                key, va = str(v).split(":", 1)
                valeur = float(va)
                if key == "temp" and valeur >= 40:
                    data1.append(v)
                elif key == "humidity" and valeur > 80:
                    data1.append(v)
                elif key == "pressure" and valeur > 2000:
                    data1.append(v)
            return data1
        elif criteria == "low":
            data2: list[Any] = []
            for v in data_batch:
                key, va = str(v).split(":", 1)
                valeur = float(va)
                if key == "temp" and valeur < 0:
                    data2.append(v)
                elif key == "humidity" and valeur <= 5:
                    data2.append(v)
                elif key == "pressure" and valeur <= 700:
                    data2.append(v)
            return data2
        return data_batch

    def process_batch(self, data_batch: list[Any]) -> str:
        """Process data."""
        i: int = 0
        for v in data_batch:
            key, valeur = str(v).split(":", 1)
            if key == "temp":
                self.temp.append(float(valeur))
                i += 1
            self.process += 1
        if i == 0:
            return (f"{self.process} readings processed,"
                    f" avg temp: temperatur dosen't existe")
        return (f"Sensor analysis: {self.process} readings processed,"
                f" avg temp: {sum(self.temp) / i}")

    def get_stats(self) -> dict[str, Union[str, int, float]]:
        """Get stats."""
        return {"sensor data": self.process}


class TransactionStream(DataStream):
    """Class Transaction Stream."""

    def __init__(self, stream_id: str, stream_type: str) -> None:
        """Init Transaction Stream."""
        super().__init__(stream_id, stream_type)
        self.buy = 0
        self.sell = 0
        self.process = 0

    def filter_data(self, data_batch: list[Any],
                    criteria: Optional[Any] = None) -> list[Any]:
        """Filtre data."""
        if criteria is None:
            return data_batch
        elif criteria == "low" or criteria == "high":
            data: list[Any] = []
            for v in data_batch:
                _, va = str(v).split(":", 1)
                valeur = float(va)
                if criteria == "high" and valeur > 200:
                    data.append(v)
                elif criteria == "low" and valeur <= 10:
                    data.append(v)
            return data
        else:
            raise Exception("The option filter is not correct")

    def process_batch(self, data_batch: list[Any]) -> str:
        """Process data."""
        for v in data_batch:
            key, valeur = str(v).split(":", 1)
            if key == "buy":
                self.buy = int(valeur) + self.buy
            elif key == "sell":
                self.sell = int(valeur) + self.sell
            self.process += 1
        if self.buy - self.sell > 0:
            return f"{self.process} operations, net flow: +{self.buy - self.sell}"
        return f"transaction analysis: {self.process} operations, net flow: {self.buy - self.sell}"

    def get_stats(self) -> dict[str, Union[str, int, float]]:
        """Get data."""
        return {"transaction data": self.process}


class EventStream(DataStream):
    """Class Event Stream."""

    def __init__(self, stream_id: str, stream_type: str) -> None:
        """Init Event Stream."""
        super().__init__(stream_id, stream_type)
        self.error = 0
        self.process = 0

    def filter_data(self, data_bench: list[Any],
                    criteria: Optional[Any] | None) -> list[Any]:
        """Filter data."""
        data: list[Any] = []
        if criteria is None:
            return data_bench
        else:
            for d in data_bench:
                if d in criteria:
                    data.append(d)
        return data

    def process_batch(self, data_batch: list[Any]) -> str:
        """Process data."""
        for v in data_batch:
            if v == "error":
                self.error += 1
            self.process += 1
        return (f"event analysis: {self.process}"
                "events, {self.error} error detected")

    def get_stats(self) -> dict[str, Union[str, int, float]]:
        """Get stats."""
        return {"Event data": self.process}


class StreamProcessor:
    """Class stream processor."""

    def __init__(self) -> None:
        """Init stream processor."""
        self.stats: dict[str, Union[str, int, float]] = {}
        self.objet_processor: list[Any] = []
        self.id_data_batch = 0
        self.sensor = 1
        self.trans = 0
        self.event = 0

    def number_data_bach(self) -> int:
        """Define Id data batch."""
        self.id_data_batch += 1
        return self.id_data_batch

    def filter_data(self, data_batch: list[Any],
                    criteria: Optional[Any] |
                    None) -> tuple[str, DataStream, str] | None:
        """Add data."""
        sensor_keys: list[str] = ["temp", "humidity", "pressure"]
        trans_keys: list[str] = ["buy", "sell", "buy"]
        event_keys: list[str] = ["login", "error", "logout"]
        if all(":" in s for s in data_batch):
            check = ":".join(data_batch).split(":")
            if any(k in check for k in sensor_keys):
                r: DataStream = SensorStream(f"SENSOR_{self.sensor}",
                                             "Environmental Data")
                self.objet_processor.append(r)
                data = r.filter_data(data_batch, criteria)
                process = r.process_batch(data)
                self.stats.update(r.get_stats())
                self.sensor += 1
                return process, r, "sensor"
            elif any(k in check for k in trans_keys):
                r: DataStream = TransactionStream(f"TRANS_{self.trans}",
                                                  "Environmental Data")
                self.objet_processor.append(r)
                data = r.filter_data(data_batch, criteria)
                process = r.process_batch(data)
                self.stats.update(r.get_stats())
                self.trans += 1
                return process, r, "transaction"
        else:
            if any(k in data_batch for k in event_keys):
                r: DataStream = EventStream(f"EVENT_{self.event}",
                                            "Environmental Data")
                self.objet_processor.append(r)
                data = r.filter_data(data_batch, criteria)
                process = r.process_batch(data)
                self.stats.update(r.get_stats())
                self.event += 1
                return process, r, "event"


def data_stream(data_batch: Any) -> None:
    """Stream data."""
    print("\n=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")
    try:
        criteria = None
        streams = StreamProcessor()
        id_data_batch: int = streams.number_data_bach()
        for d in data_batch:
            p, stream, t = streams.filter_data(d, criteria)
            print(f"\nInitializing {str(t).capitalize()} Stream...")
            stream: DataStream
            print(f"Stream ID: {stream.stream_id}, Type: {stream.stream_type}")
            print(f"Processing {t} batch: {d}")
            print(p)

        print("\n=== Polymorphic Stream Processing ===")
        print("Processing mixed stream types through unified interface...\n")
        print(f"Batch {id_data_batch} Results:")
        for s, i in streams.stats.items():
            if s == "Sensor data:":
                print(f"- {s.capitalize()} : {i} readings processed")
            elif s == "Transaction data":
                print(f"- {s.capitalize()} : {i} operations processed")
            else:
                print(f"- {s.capitalize()} : {i} events processed")
        
        criteria: str = "high"
        print(f"\nStream filtering active: {criteria}-priority data only")
        print("Filtered results:", end="")
        for d in data_batch:
            _, stream, t = streams.filter_data(d, criteria)
            if t in "sensor data".split(" ", -1):
                stats = stream.get_stats()
                print(f" {stats.get('sensor data')}"
                      "critical sensor alerts,", end="")
            elif t in "transaction data":
                stats = stream.get_stats()
                print(f" {stats.get('transaction data')}"
                      " large transaction", end="")
                print()
        print("\nAll streams processed successfully. Nexus throughput optimal.\n")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    data_batch: list[Any] = [
        ["temp:50", "humidity:65", "pressure:1013", "humidity:65"],
        ["buy:100", "sell:170", "buy:3000"],
        ["login", "error", "logout"]
    ]
    data_stream(data_batch)
