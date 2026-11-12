"""Demostración ejecutable con datos sintéticos."""

import argparse
import json
from dataclasses import asdict

from .simulator import Package, Station


def main() -> None:
    parser = argparse.ArgumentParser(description="Simula un lote OpenSort.")
    parser.add_argument("--scenario", choices=["demo", "wrong-exit"], default="demo")
    args = parser.parse_args()

    station = Station(
        manifest={
            "PKG-001": "VERACRUZ", "PKG-002": "PUEBLA",
            "PKG-003": "MERIDA", "PKG-004": "XALAPA",
        },
        routes={"VERACRUZ": "A", "PUEBLA": "B", "MERIDA": "C"},
    )
    packages = [
        Package("PKG-001", "A"),
        Package("PKG-002", "B"),
        Package("PKG-999", "REVISION"),
        Package(None, "REVISION"),
        Package("PKG-004", "REVISION"),
        Package("PKG-003", "A" if args.scenario == "wrong-exit" else None),
        Package("PKG-001", "A"),
    ]
    for event in station.run(packages):
        print(json.dumps(asdict(event), ensure_ascii=False))


if __name__ == "__main__":
    main()
