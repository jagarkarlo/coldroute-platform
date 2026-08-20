# ColdRoute Platform

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img alt="License" src="https://img.shields.io/badge/License-MIT-3FB950?style=for-the-badge" />
</p>

ColdRoute Platform is a fictional, production-shaped Kubernetes platform for
processing and operating cold-chain telemetry workloads.

The project will demonstrate a complete platform engineering workflow across
application delivery, GitOps, observability, security, progressive delivery,
and disaster recovery.

## Planned Architecture

```mermaid
flowchart LR
    Simulator[Device simulator] --> Gateway[Telemetry gateway]
    Gateway --> Stream[Event stream]
    Stream --> Processor[Excursion processor]
    Processor --> Store[(Telemetry store)]
    Store --> Console[Operations console]

    Platform[Platform services] --> Observability[Metrics, logs, and traces]
    GitOps[GitOps controller] --> Platform
```

## Project Status

Milestone 1 is in progress. The repository currently contains a deterministic
Python device simulator that emits newline-delimited JSON telemetry. Application
services, storage, Kubernetes manifests, infrastructure modules, and automated
delivery workflows will be introduced in small, independently verifiable
milestones.

## Device Simulator

The first component models a refrigerated shipment sensor. It produces a stable
event contract with configurable temperature drift and seeded jitter, allowing
later services and tests to replay the same telemetry sequence.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
coldroute-simulate --count 3 --seed 42
```

Run the tests with the Python standard library:

```bash
python -m unittest discover -s tests -v
```

The next milestone will introduce an HTTP telemetry gateway that accepts this
event contract. No database, message broker, or Kubernetes resources are part of
the project yet.

## Public-Safety Boundary

All infrastructure, telemetry, identities, endpoints, and operational scenarios
in this repository are fictional. The project will not contain credentials,
customer data, employer configuration, or production access details.
