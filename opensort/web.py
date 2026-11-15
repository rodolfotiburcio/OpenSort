"""Simulación temporal y servidor HTTP local, solo biblioteca estándar."""
import json
import threading
import time
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files

from .simulator import Station

EXITS = ["A", "B", "C", "REVISION"]
MANIFEST = {"PKG-001": "VERACRUZ", "PKG-002": "PUEBLA", "PKG-003": "MERIDA", "PKG-004": "XALAPA"}
ROUTES = {"VERACRUZ": "A", "PUEBLA": "B", "MERIDA": "C"}

class Simulation:
    def __init__(self):
        self.station = Station(MANIFEST, ROUTES)
        self.queue = []
        self.events = []
        self.active = None
        self.elapsed = 0.0
        self.paused = True
        self.speed = 1.0
        self.sensors = {name: False for name in ["ENTRY", *EXITS]}
        self.inspected = False
        self.button_down = False
        self.completed = {"sorted": 0, "sent_to_review": 0, "station_blocked": 0}

    def record(self, events):
        for event in events:
            self.events.append({**asdict(event), "sequence": len(self.events) + 1})
            if event.event in self.completed:
                self.completed[event.event] += 1

    def advance(self, seconds):
        if self.paused or self.station.state == "blocked":
            return
        if self.active is None and self.queue:
            item = self.queue.pop(0)
            self.record(self.station.start(item["qr"], item["manifest_available"]))
            self.active = {**item, "expected": self.station.current.expected_exit,
                           "attempt_id": self.station.current.attempt_id, "progress": 0}
            self.elapsed = 0
            self.inspected = False
        if self.active is None:
            return
        self.elapsed += seconds * self.speed
        progress = min(1, self.elapsed / 6)
        item = self.active
        item["progress"] = min(progress, .78) if item["fault"] == "timeout" else progress
        self.sensors = {name: False for name in self.sensors}
        self.sensors["ENTRY"] = progress < .12
        if progress >= .94 and item["fault"] != "timeout":
            self.sensors[item["wrong_exit"] if item["fault"] == "wrong_exit" else item["expected"]] = True
        if self.elapsed >= 6:
            observed = (None if item["fault"] == "timeout" else
                        item["wrong_exit"] if item["fault"] == "wrong_exit" else item["expected"])
            if observed:
                self.sensors[observed] = True
            self.record(self.station.finish(observed))
            if self.station.state == "blocked":
                self.paused = True
            else:
                self.active = None
                self.sensors = {name: False for name in self.sensors}

    def command(self, data):
        action = data.get("action")
        if action == "enqueue":
            qr = data.get("qr")
            if qr is not None and (not isinstance(qr, str) or not qr.strip() or len(qr) > 80):
                raise ValueError("ID inválido")
            fault = data.get("fault", "none")
            wrong = data.get("wrong_exit", "B")
            available = data.get("manifest_available", True)
            if fault not in ["none", "timeout", "wrong_exit"] or wrong not in EXITS or type(available) is not bool:
                raise ValueError("Condiciones de intento inválidas")
            destination = MANIFEST.get(qr) if available and qr else None
            expected = ROUTES.get(destination, "REVISION")
            if fault == "wrong_exit" and wrong == expected:
                raise ValueError("Elige una salida distinta de la esperada")
            if len(self.queue) >= 100:
                raise ValueError("La cola está llena")
            self.queue.append({"qr": qr, "fault": fault, "wrong_exit": wrong, "manifest_available": available})
        elif action == "demo":
            if len(self.queue) > 93:
                raise ValueError("La cola está llena")
            for qr in ["PKG-001", "PKG-002", "PKG-999", None, "PKG-004", "PKG-003", "PKG-001"]:
                self.queue.append({"qr": qr, "fault": "timeout" if qr == "PKG-003" else "none",
                                   "wrong_exit": "A", "manifest_available": True})
        elif action == "play":
            if self.station.state == "blocked":
                raise ValueError("La estación requiere rearme")
            self.paused = False
        elif action == "pause":
            self.paused = True
        elif action == "speed":
            if data.get("value") not in [.5, 1, 2]:
                raise ValueError("Velocidad inválida")
            self.speed = data["value"]
        elif action == "clear":
            if self.station.state != "blocked":
                raise ValueError("El despeje solo se permite tras un bloqueo")
            self.active = None
            self.sensors = {name: False for name in self.sensors}
            self.inspected = True
        elif action == "sensor":
            if self.station.state != "blocked" or data.get("name") not in self.sensors or type(data.get("occupied")) is not bool:
                raise ValueError("Sensor o estado inválido")
            self.sensors[data["name"]] = data["occupied"]
        elif action == "reset_down":
            if not self.button_down:
                self.button_down = True
                self.record(self.station.reset(not self.sensors["ENTRY"],
                    not any(self.sensors[name] for name in EXITS), self.inspected))
        elif action == "reset_up":
            self.button_down = False
        else:
            raise ValueError("Comando desconocido")

    def snapshot(self):
        return {"state": self.station.state, "paused": self.paused, "speed": self.speed,
                "active": self.active, "queue": self.queue, "sensors": self.sensors,
                "inspected": self.inspected, "button_down": self.button_down,
                "events": self.events, "counts": self.completed,
                "failed": asdict(self.station.failed) if self.station.failed else None}


def make_server(port=8000):
    simulation = Simulation()
    lock = threading.Lock()
    class Handler(BaseHTTPRequestHandler):
        def reply(self, code, body, mime="application/json; charset=utf-8"):
            payload = json.dumps(body, ensure_ascii=False).encode() if isinstance(body, dict) else body
            self.send_response(code)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self):
            if self.path == "/api/state":
                with lock:
                    self.reply(200, simulation.snapshot())
            elif self.path in ["/", "/app.js", "/style.css"]:
                name = "index.html" if self.path == "/" else self.path[1:]
                mime = {"index.html": "text/html", "app.js": "text/javascript", "style.css": "text/css"}[name]
                self.reply(200, files("opensort").joinpath("static", name).read_bytes(), mime + "; charset=utf-8")
            else:
                self.reply(404, {"error": "No encontrado"})

        def do_POST(self):
            if self.path != "/api/commands":
                return self.reply(404, {"error": "No encontrado"})
            try:
                length = int(self.headers.get("Content-Length", 0))
                if not 0 < length <= 4096:
                    raise ValueError("Tamaño de comando inválido")
                data = json.loads(self.rfile.read(length))
                if not isinstance(data, dict):
                    raise ValueError("Se requiere un objeto JSON")
                with lock:
                    simulation.command(data)
                    self.reply(200, simulation.snapshot())
            except (ValueError, TypeError) as error:
                self.reply(400, {"error": str(error)})

        def log_message(self, *args):
            pass
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    return server, simulation, lock


def serve(port=8000):
    server, simulation, lock = make_server(port)
    stop = threading.Event()
    def clock():
        previous = time.monotonic()
        while not stop.wait(.05):
            now = time.monotonic()
            with lock:
                simulation.advance(now - previous)
            previous = now
    ticker = threading.Thread(target=clock, daemon=True)
    ticker.start()
    print(f"OpenSort 2D: http://127.0.0.1:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        ticker.join()
        server.server_close()
