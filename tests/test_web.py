import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from opensort.simulator import Package, Station
from opensort.web import EXITS, MANIFEST, ROUTES, Simulation, make_server


class RecoveryTests(unittest.TestCase):
    def test_block_persists_and_failure_survives_reset(self):
        station = Station(MANIFEST, ROUTES)
        failure = station.run([Package('PKG-001', None)])[-1]
        self.assertEqual(station.run([Package('PKG-002', 'B')]), [])
        self.assertEqual(station.reset(False, True)[0].event, 'reset_rejected')
        self.assertEqual(station.state, 'blocked')
        self.assertEqual(station.reset(True, True)[0].event, 'reset_accepted')
        self.assertEqual(station.failed, failure)
        self.assertEqual(station.run([Package('PKG-002', 'B')])[-1].event, 'sorted')

    def test_routes_and_review_require_confirmation(self):
        cases = [('PKG-001', True, 'A'), ('PKG-002', True, 'B'),
                 ('PKG-003', True, 'C'), ('PKG-004', True, 'REVISION'),
                 ('PKG-999', True, 'REVISION'), (None, True, 'REVISION'),
                 ('PKG-001', False, 'REVISION')]
        for qr, available, expected in cases:
            with self.subTest(qr=qr, available=available):
                station = Station(MANIFEST, ROUTES)
                self.assertEqual(station.start(qr, available)[-1].expected_exit, expected)
                self.assertEqual(station.state, 'processing')
                self.assertEqual(station.finish(None)[-1].event, 'station_blocked')


class SimulationTests(unittest.TestCase):
    def setUp(self):
        self.sim = Simulation()

    def command(self, action, **kwargs):
        self.sim.command({'action': action, **kwargs})

    def fail(self):
        self.command('enqueue', qr='PKG-001', fault='timeout')
        self.command('enqueue', qr='PKG-002')
        self.command('play')
        self.sim.advance(6)
        self.assertEqual(self.sim.station.state, 'blocked')
        self.assertEqual(len(self.sim.queue), 1)

    def test_pause_and_speed(self):
        self.command('enqueue', qr='PKG-001')
        self.sim.advance(10)
        self.assertIsNone(self.sim.active)
        self.command('play')
        self.sim.advance(1)
        self.command('pause')
        self.sim.advance(10)
        self.assertEqual(self.sim.elapsed, 1)
        self.command('speed', value=2)
        self.command('play')
        self.sim.advance(2.5)
        self.assertEqual(self.sim.completed['sorted'], 1)

    def test_rejected_held_reset_needs_new_press(self):
        self.fail()
        self.command('reset_down')
        self.assertEqual(self.sim.events[-1]['reason'], 'inspection_required')
        self.command('clear')
        self.command('reset_down')
        self.assertEqual(self.sim.station.state, 'blocked')
        self.command('reset_up')
        self.command('sensor', name='C', occupied=True)
        self.command('reset_down')
        self.assertEqual(self.sim.events[-1]['reason'], 'sensors_occupied')
        self.command('sensor', name='C', occupied=False)
        self.sim.advance(20)
        self.command('reset_down')
        self.assertEqual(self.sim.station.state, 'blocked')
        self.command('reset_up')
        self.command('reset_down')
        self.assertEqual(self.sim.station.state, 'available')
        self.assertTrue(self.sim.paused)
        self.assertIsNotNone(self.sim.station.failed)
        self.sim.advance(20)
        self.assertEqual(len(self.sim.queue), 1)
        self.command('reset_up')
        self.command('play')
        self.sim.advance(6)
        self.assertEqual(self.sim.completed['sorted'], 1)

    def test_press_before_block_does_not_reset(self):
        self.command('reset_down')
        self.fail()
        self.command('clear')
        self.command('reset_down')
        self.assertEqual(self.sim.station.state, 'blocked')
        self.command('reset_up')
        self.command('reset_down')
        self.assertEqual(self.sim.station.state, 'available')

    def test_wrong_exit_and_invalid_commands(self):
        self.command('enqueue', qr='PKG-001', fault='wrong_exit', wrong_exit='C')
        self.command('play')
        self.sim.advance(6)
        self.assertTrue(self.sim.sensors['C'])
        self.assertEqual(self.sim.events[-1]['observed_exit'], 'C')
        self.assertEqual(self.sim.events[-1]['reason'], 'wrong_exit')
        for data in [{'action': 'play'}, {'action': 'speed', 'value': 9},
                     {'action': 'enqueue', 'qr': [], 'fault': 'none'},
                     {'action': 'enqueue', 'qr': 'PKG-001', 'fault': 'wrong_exit', 'wrong_exit': 'A'},
                     {'action': 'unknown'}]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                self.sim.command(data)


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server, cls.sim, cls.lock = make_server(0)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()
        cls.server.server_close()

    def test_static_state_and_commands(self):
        for path in ['/', '/app.js', '/style.css']:
            with urlopen(self.base + path) as response:
                self.assertEqual(response.status, 200)
                self.assertGreater(len(response.read()), 100)
        with urlopen(self.base + '/api/state') as response:
            self.assertEqual(json.load(response)['state'], 'available')
        request = Request(self.base + '/api/commands', data=b'{"action":"enqueue","qr":"PKG-002"}',
                          headers={'Content-Type': 'application/json'})
        with urlopen(request) as response:
            self.assertEqual(json.load(response)['queue'][0]['qr'], 'PKG-002')
        for payload in [b'[]', b'bad json', b'{"action":"bad"}']:
            with self.subTest(payload=payload), self.assertRaises(HTTPError) as caught:
                urlopen(Request(self.base + '/api/commands', data=payload))
            self.assertEqual(caught.exception.code, 400)
        with self.assertRaises(HTTPError) as caught:
            urlopen(self.base + '/../../pyproject.toml')
        self.assertEqual(caught.exception.code, 404)
