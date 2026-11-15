"""Demostración ejecutable con datos sintéticos."""

import argparse
import json
from dataclasses import asdict

from .simulator import Package, Station


def main() -> None:
    parser = argparse.ArgumentParser(description="Simula un lote OpenSort.")
    parser.add_argument("--scenario", choices=["demo", "wrong-exit"], default="demo")
    parser.add_argument("--web", action="store_true", help="Abre el servidor de simulación 2D local")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if args.web:
        from .web import serve
        if not 0 <= args.port <= 65535:
            parser.error("El puerto debe estar entre 0 y 65535")
        try:
            serve(args.port)
        except OSError as error:
            parser.exit(1, f"No se pudo iniciar el servidor: {error}. Prueba --port 8001.\n")
        return

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
