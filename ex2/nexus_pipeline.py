#!/usr/bin/env python3
"""Process Pipline."""
from typing import Any, Optional, Protocol, Union
from abc import ABC, abstractmethod
import time


class ProcessingPipeline(ABC):
    """Class Processing Pipline."""

    def __init__(self) -> None:
        """Init Processing Pipline."""
        self.stage: tuple[ProcessingStage, ...] = (
            InputStage(), TransformStage(), OutputStage()
        )

    def add_stage(self, data: dict, finaly: Optional[bool] = None) -> Any:
        """Add stage."""
        for stage in self.stage:
            data = stage.process(data, finaly)
        return data

    @abstractmethod
    def process(self, data: Any) -> Union[str, Any]:
        """Process data."""
        pass


class JSONAdapter(ProcessingPipeline):
    """Init JSON Adapter."""

    def __init__(self, pipline_id: str) -> None:
        """Init JSON Adapter."""
        super().__init__()
        self.pipline_id = pipline_id

    def process(self, data: Any,
                finaly: Optional[bool] = None) -> Union[str, Any]:
        """Process data."""
        normalize = {"source": "JSON", "row": [data]}
        return self.add_stage(normalize, finaly)


class CSVAdapter(ProcessingPipeline):
    """Init CSV Adapter."""

    def __init__(self, pipline_id: str) -> None:
        """Init JSON Adapter."""
        super().__init__()
        self.pipline_id = pipline_id

    def process(self, data: Any,
                finaly: Optional[bool] = None) -> Union[str, Any]:
        """Process data."""
        normalize = {"source": "CSV", "header": "user, action, timestamp",
                     "row": [data]}
        return self.add_stage(normalize, finaly)


class StreamAdapter(ProcessingPipeline):
    """Class Stream adapter"""

    def __init__(self, pipline_id: str) -> None:
        """Init JSON Adapter."""
        super().__init__()
        self.pipline_id = pipline_id

    def process(self, data: Any,
                finaly: Optional[bool] = None) -> Union[str, Any]:
        """Process data."""
        header = "".join(d for d in data if isinstance(d, str))
        if not header:
            header = "Real-time sensor stream"
        value = [d for d in data if "value" in d]
        normalize = {"source": "stream", "header": header, "row": value}
        return self.add_stage(normalize, finaly)


class ProcessingStage(Protocol):
    """Init Process Stage."""

    def process(self, data: Any, finaly: Optional[bool] = None) -> Any:
        """Process data."""
        pass


class InputStage:
    """Class Input Stage."""

    def process(self, data: Any, finaly: Optional[bool] = None) -> dict:
        """Process data."""
        if not data:
            raise Exception("Error detected in Stage 1: No data in records")
        elif data["source"] == "JSON":
            for d in data["row"]:
                if finaly:
                    print(f"Input: {d}")
                if len(d) == 0:
                    raise Exception("Error detected in Stage 1:"
                                    " No data in records")
        elif data["source"] == "CSV":
            if finaly:
                print(f"Input: {data["header"]}")
            if len(data["row"]) == 0:
                raise Exception("Error detected in Stage 1:"
                                " No data in records")
        elif data["source"] == "stream":
            if finaly:
                print(f"Input: {data["header"]}")
            if len(data["row"]) == 0:
                raise Exception("Error detected in Stage 1:"
                                " No data in records")
        return data


class TransformStage:
    """Class Transfom Stage."""

    def process(self, data: Any, finaly: Optional[bool] = None) -> dict:
        """Process data."""
        if data['source'] == "JSON":
            total: int = 0
            for d in data["row"]:
                records = d
                if not isinstance(records['value'], (float, int)):
                    raise Exception("Error detected in Stage 2: "
                                    "Invalid data format\n"
                                    "Recovery initiated: "
                                    "Switching to backup processor\n"
                                    "Recovery successful:"
                                    " Pipeline restored"
                                    ", processing resumed\n")
                total = d.get("value") + total
            avg = (total / len(data["row"]))
            data["avg"] = avg
            data["unit"] = "°C"
            if avg > 40:
                data['status'] = "(high range)"
            elif avg < 6:
                data['status'] = "(low range)"
            elif avg >= 6 and avg <= 40:
                data['status'] = "(medium range)"
            if finaly:
                print("Transform: Enriched with metadata and validation")
            return data
        elif data["source"] == "CSV":
            for d in data["row"]:
                list_data = d.split("\n")
                for s in list_data:
                    nbr_elements = len(s.split(","))
                    if nbr_elements < 3:
                        raise Exception("Error detected in Stage 2: "
                                        "Invalid data format\n"
                                        "Recovery initiated: "
                                        "Switching to backup processor\n"
                                        "Recovery successful: Pipeline"
                                        "restored, processing resumed\n"
                                        )
            user_activity = len(list_data)
            if not any("," in d for d in data["row"]):
                raise Exception("Error detected in Stage 2: "
                                "Invalid data format\n"
                                "Recovery initiated: "
                                "Switching to backup processor\n"
                                "Recovery successful: Pipeline restored"
                                ", processing resumed\n")
            data["activity"] = user_activity
            if finaly:
                print("Transform: Parsed and structured data")
            return data
        elif data["source"] == "stream":
            if not (isinstance(d, dict) for d in data["row"]):
                raise Exception("Error detected in Stage 2: "
                                "Invalid data format\n"
                                "Recovery initiated: "
                                "Switching to backup processor\n"
                                "Recovery successful: Pipeline restored"
                                ", processing resumed\n")
            total = 0
            for s in data["row"]:
                total = s.get("value") + total
            reading = len(data["row"])
            data["reading"] = reading
            data["avg"] = total / reading
            data["unit"] = "°C"
            if finaly:
                print("Transform: Aggregated and filtered")
            return data
        return data


class AnalyzeStage:
    """Class Analyze Stage."""

    def process(self, data: Any) -> dict:
        "Analyze error"
        try:
            if data["source"] == "JSON":
                total = len(data["row"])
                if total == 0:
                    raise ZeroDivisionError(
                        "Error detected in Stage Analyze: "
                        "not data in row, division zero not possible"
                    )
                succes = sum(1 for d in data["row"] if isinstance(d, dict))
                efficiency = succes / total * 100
                data["efficiency"] = efficiency
                data["records"] = total
            elif data["source"] == "CSV":
                for d in data["row"]:
                    list_data = str(d).split("\n")
                total = len(list_data)
                if total == 0:
                    raise ZeroDivisionError(
                        "Error detected in Stage Analyze: "
                        "not data in row, division zero not possible"
                    )
                succes = sum(1 for d in list_data if isinstance(d, str))
                efficiency = succes / total * 100
                data["efficiency"] = efficiency
                data["records"] = total
            elif data["source"] == "stream":
                total = len(list_data)
                if total == 0:
                    raise ZeroDivisionError(
                        "Error detected in Stage Analyze: "
                        "not data in row, division zero not possible"
                    )
                succes = sum(1 for d in list_data if isinstance(d, dict))
                efficiency = succes / total * 100
                data["efficiency"] = efficiency
                data["records"] = total
        except Exception as e:
            print(e)
        return data


class OutputStage:
    """Class Output Stage."""

    def process(self, data: Any, finaly: Optional[bool] = None) -> str:
        """Process data."""
        if finaly is False:
            return data
        if not data or not isinstance(data, dict):
            return ("Error Type data: The data is not JSON, CSV or Stream")
        elif data["source"] == "JSON" and finaly:
            return (
                f"Processed temperature reading:"
                f" {data["avg"]}{data['unit']} {data['status']}"
            )
        elif data["source"] == "CSV" and finaly:
            return (
                f"User activity logged: {data["activity"]} actions processed"
            )
        elif data["source"] == "stream" and finaly:
            return (
                f"Stream summary: {data["reading"]},"
                f" avg: {data["avg"]}{data["unit"]}"
            )
        return (
            f"Chain result: {data["records"]} records"
            " processed through 3-stage pipeline"
        )


class NexusManager:
    """Class Nexus Manager."""

    def __init__(self) -> None:
        """Init Nexus Manager."""
        self.pipline_json = 0
        self.pipline_csv = 0
        self.pipline_stream = 0

    def handle(self, data: Any,
               finaly: Optional[bool] = None) -> Union[str, Any]:
        """Handle Nexus Process."""
        try:
            if isinstance(data, dict):
                if finaly:
                    print("\nProcessing JSON data through pipeline...")
                self.pipline_json += 1
                json = JSONAdapter(f"JSON {self.pipline_json}")
                return json.process(data, finaly)
            elif isinstance(data, str):
                self.pipline_csv += 1
                if finaly:
                    print("\nProcessing CSV data through same pipeline...")
                csv = CSVAdapter(f"CSV {self.pipline_csv}")
                return csv.process(data, finaly)
            elif isinstance(data, list):
                self.pipline_stream += 1
                if finaly:
                    print("\nProcessing Stream data through same pipeline...")
                stream = StreamAdapter(f"Stream {self.pipline_stream}")
                return stream.process(data, finaly)
            raise Exception("Nexus Error: The data is not CSV, JSON or Stream")
        except Exception as e:
            print(f"{e}")
        return None


def nexus_pipeline(data: list[Any]) -> None:
    """Process pipline."""
    print("=== CODE NEXUS - ENTERPRISE PIPELINE SYSTEM ===\n")
    print("Initializing Nexus Manager...")
    print("Pipeline capacity: 1000 streams/second\n")
    print("Creating Data Processing Pipeline...")
    print("Stage 1: Input validation and parsing")
    print("Stage 2: Data transformation and enrichment")
    print("Stage 3: Output formatting and delivery\n")

    print("=== Multi-Format Data Processing ===")
    nexus = NexusManager()
    for d in data:
        result = nexus.handle(d, True)
        if result:
            print(result)

    print("\n=== Pipeline Chaining Demo ===")
    print("Pipeline A → Pipeline B → Pipeline C")
    print("Data flow: Raw → Processed → Analyzed → Stored")
    json = {"sensor": "temp", "value": 7, "unit": "°C"}
    start = time.perf_counter()
    piplineA = nexus.handle(json, False)
    piplineB = AnalyzeStage().process(piplineA)
    piplineC = OutputStage().process(piplineB)
    fin = time.perf_counter() - start
    print(f"\n{piplineC}")
    print(
        f"Performance: {piplineB["efficiency"]:.0f}%, "
        f"{round(fin, 5):.5f}s total processing time"
    )
    print("\n=== Error Recovery Test ===")
    try:
        error: str = "samet login 10.3"
        print("Simulating pipeline failure...")
        nexus.handle(error)
        print("Nexus Integration complete. All systems operational.")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    data: list[Any] = [
        {"sensor": "temp", "value": 7, "unit": "°C"},
        "user action timestamp",
        "login, 10.3\nsamet, login, 11",
        [{"sensor": "temp", "value": 80, "unit": "°C"},
         {"sensor": "temp", "value": 30, "unit": "°C"}]
    ]
    nexus_pipeline(data)
