from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json

from coldroute_simulator.telemetry import SimulatorConfig, generate_events


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Emit fictional cold-chain telemetry as newline-delimited JSON."
    )
    parser.add_argument("--device-id", default="reefer-001")
    parser.add_argument("--shipment-id", default="shipment-001")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starting-temperature", type=float, default=3.0)
    parser.add_argument("--drift-per-reading", type=float, default=0.0)
    parser.add_argument("--jitter", type=float, default=0.2)
    parser.add_argument("--interval-seconds", type=int, default=30)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = SimulatorConfig(
        device_id=args.device_id,
        shipment_id=args.shipment_id,
        starting_temperature_celsius=args.starting_temperature,
        drift_per_reading=args.drift_per_reading,
        jitter_celsius=args.jitter,
        interval_seconds=args.interval_seconds,
    )

    for event in generate_events(
        config,
        args.count,
        seed=args.seed,
        started_at=datetime.now(timezone.utc),
    ):
        print(json.dumps(event.to_dict(), separators=(",", ":")))


if __name__ == "__main__":
    main()