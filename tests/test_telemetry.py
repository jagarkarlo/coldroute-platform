from datetime import datetime, timezone
import unittest

from coldroute_simulator.telemetry import SimulatorConfig, generate_events


class GenerateEventsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.started_at = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)

    def test_generates_stable_event_contract(self) -> None:
        config = SimulatorConfig(jitter_celsius=0, interval_seconds=15)

        events = list(generate_events(config, 2, started_at=self.started_at))

        self.assertEqual(events[0].to_dict(), {
            "schema_version": "1.0",
            "device_id": "reefer-001",
            "shipment_id": "shipment-001",
            "sequence": 0,
            "recorded_at": "2026-01-01T12:00:00+00:00",
            "temperature_celsius": 3.0,
        })
        self.assertEqual(events[1].sequence, 1)
        self.assertEqual(events[1].recorded_at, "2026-01-01T12:00:15+00:00")

    def test_seed_reproduces_temperature_sequence(self) -> None:
        config = SimulatorConfig(drift_per_reading=0.5)

        first_run = list(generate_events(config, 3, seed=42, started_at=self.started_at))
        second_run = list(generate_events(config, 3, seed=42, started_at=self.started_at))

        self.assertEqual(first_run, second_run)
        self.assertEqual(
            [event.temperature_celsius for event in first_run],
            [3.06, 3.31, 3.91],
        )

    def test_rejects_invalid_configuration(self) -> None:
        with self.assertRaisesRegex(ValueError, "interval_seconds must be positive"):
            SimulatorConfig(interval_seconds=0)

        with self.assertRaisesRegex(ValueError, "started_at must include a timezone"):
            list(generate_events(SimulatorConfig(), 1, started_at=datetime(2026, 1, 1)))


if __name__ == "__main__":
    unittest.main()