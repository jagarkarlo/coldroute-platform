from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
import random
from typing import Iterator


@dataclass(frozen=True)
class SimulatorConfig:
    device_id: str = "reefer-001"
    shipment_id: str = "shipment-001"
    starting_temperature_celsius: float = 3.0
    drift_per_reading: float = 0.0
    jitter_celsius: float = 0.2
    interval_seconds: int = 30

    def __post_init__(self) -> None:
        if not self.device_id.strip():
            raise ValueError("device_id must not be empty")
        if not self.shipment_id.strip():
            raise ValueError("shipment_id must not be empty")
        if self.jitter_celsius < 0:
            raise ValueError("jitter_celsius must be non-negative")
        if self.interval_seconds <= 0:
            raise ValueError("interval_seconds must be positive")


@dataclass(frozen=True)
class TelemetryEvent:
    schema_version: str
    device_id: str
    shipment_id: str
    sequence: int
    recorded_at: str
    temperature_celsius: float

    def to_dict(self) -> dict[str, str | int | float]:
        return asdict(self)


def generate_events(
    config: SimulatorConfig,
    count: int,
    *,
    seed: int = 0,
    started_at: datetime | None = None,
) -> Iterator[TelemetryEvent]:
    if count < 0:
        raise ValueError("count must be non-negative")

    start = started_at or datetime.now(timezone.utc)
    if start.tzinfo is None:
        raise ValueError("started_at must include a timezone")

    random_source = random.Random(seed)
    for sequence in range(count):
        jitter = random_source.uniform(-config.jitter_celsius, config.jitter_celsius)
        temperature = (
            config.starting_temperature_celsius
            + config.drift_per_reading * sequence
            + jitter
        )
        recorded_at = start + timedelta(seconds=config.interval_seconds * sequence)

        yield TelemetryEvent(
            schema_version="1.0",
            device_id=config.device_id,
            shipment_id=config.shipment_id,
            sequence=sequence,
            recorded_at=recorded_at.isoformat(),
            temperature_celsius=round(temperature, 2),
        )