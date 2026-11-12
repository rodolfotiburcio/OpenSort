"""Clasificación secuencial de paquetes con confirmación de salida simulada."""

from dataclasses import dataclass
from uuid import uuid4

REVIEW_EXIT = "REVISION"


@dataclass(frozen=True)
class Package:
    qr: str | None
    observed_exit: str | None


@dataclass(frozen=True)
class Event:
    attempt_id: str
    package_id: str | None
    event: str
    destination: str | None = None
    expected_exit: str | None = None
    observed_exit: str | None = None
    reason: str | None = None


class Station:
    def __init__(self, manifest: dict[str, str], routes: dict[str, str]):
        self.manifest = dict(manifest)
        self.routes = dict(routes)

    def run(self, packages: list[Package]) -> list[Event]:
        events = []
        for package in packages:
            attempt_id = str(uuid4())
            events.append(Event(attempt_id, package.qr, "package_detected"))
            destination = self.manifest.get(package.qr) if package.qr else None
            exit_id = self.routes.get(destination) if destination is not None else None

            reason = None
            if not package.qr:
                reason = "unreadable_qr"
            elif destination is None:
                reason = "unknown_package"
            elif exit_id is None:
                reason = "unmapped_destination"

            expected_exit = exit_id if exit_id is not None else REVIEW_EXIT
            events.append(Event(
                attempt_id, package.qr, "route_selected", destination,
                expected_exit, reason=reason,
            ))

            if package.observed_exit != expected_exit:
                failure = "exit_timeout" if package.observed_exit is None else "wrong_exit"
                events.append(Event(
                    attempt_id, package.qr, "station_blocked", destination,
                    expected_exit, package.observed_exit, failure,
                ))
                break

            outcome = "sent_to_review" if reason else "sorted"
            events.append(Event(
                attempt_id, package.qr, outcome, destination,
                expected_exit, package.observed_exit, reason,
            ))

        return events
