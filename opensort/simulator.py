"""Clasificación secuencial con estado persistente y confirmación independiente."""
from dataclasses import dataclass, replace
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
        self.state = "available"
        self.current: Event | None = None
        self.failed: Event | None = None

    def start(self, qr: str | None, manifest_available: bool = True) -> list[Event]:
        if self.state != "available":
            return []
        destination = self.manifest.get(qr) if qr and manifest_available else None
        exit_id = self.routes.get(destination) if destination is not None else None
        reason = ("unreadable_qr" if not qr else "manifest_unavailable" if not manifest_available
                  else "unknown_package" if destination is None else
                  "unmapped_destination" if exit_id is None else None)
        attempt = str(uuid4())
        self.current = Event(attempt, qr, "route_selected", destination,
                             exit_id if exit_id is not None else REVIEW_EXIT, reason=reason)
        self.state = "processing"
        return [Event(attempt, qr, "package_detected"), self.current]

    def finish(self, observed_exit: str | None) -> list[Event]:
        if self.state != "processing" or self.current is None:
            return []
        route = self.current
        if observed_exit != route.expected_exit:
            result = replace(route, event="station_blocked", observed_exit=observed_exit,
                             reason="exit_timeout" if observed_exit is None else "wrong_exit")
            self.state = "blocked"
            self.failed = result
        else:
            result = replace(route, event="sent_to_review" if route.reason else "sorted",
                             observed_exit=observed_exit)
            self.state = "available"
        self.current = None
        return [result]

    def reset(self, entry_clear: bool, exits_clear: bool, inspected: bool = True) -> list[Event]:
        if self.state != "blocked" or self.failed is None:
            return []
        accepted = entry_clear and exits_clear and inspected
        result = replace(self.failed, event="reset_accepted" if accepted else "reset_rejected",
                         reason=None if accepted else "inspection_required" if not inspected else "sensors_occupied")
        if accepted:
            self.state = "available"
        return [result]

    def run(self, packages: list[Package]) -> list[Event]:
        events: list[Event] = []
        for package in packages:
            started = self.start(package.qr)
            if not started:
                break
            events.extend(started)
            events.extend(self.finish(package.observed_exit))
            if self.state == "blocked":
                break
        return events
