import unittest

from opensort.simulator import Package, Station


class StationTests(unittest.TestCase):
    def setUp(self):
        self.station = Station(
            {"PKG-001": "VERACRUZ", "PKG-002": "XALAPA"},
            {"VERACRUZ": "A"},
        )

    def test_success_requires_expected_exit(self):
        events = self.station.run([Package("PKG-001", "A")])
        self.assertEqual(
            [event.event for event in events],
            ["package_detected", "route_selected", "sorted"],
        )
        self.assertEqual(events[-1].observed_exit, "A")

    def test_review_reasons(self):
        for qr, reason in [
            (None, "unreadable_qr"),
            ("PKG-999", "unknown_package"),
            ("PKG-002", "unmapped_destination"),
        ]:
            with self.subTest(qr=qr):
                result = self.station.run([Package(qr, "REVISION")])[-1]
                self.assertEqual(result.event, "sent_to_review")
                self.assertEqual(result.reason, reason)

    def test_timeout_and_wrong_exit_block_next_package(self):
        for observed_exit, reason in [(None, "exit_timeout"), ("B", "wrong_exit")]:
            with self.subTest(observed_exit=observed_exit):
                events = self.station.run([
                    Package("PKG-001", observed_exit),
                    Package("PKG-999", "REVISION"),
                ])
                self.assertEqual(events[-1].event, "station_blocked")
                self.assertEqual(events[-1].reason, reason)
                self.assertEqual(len(events), 3)

    def test_reprocessing_uses_a_new_attempt(self):
        events = self.station.run([Package("PKG-001", "A")] * 2)
        results = [event for event in events if event.event == "sorted"]
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].package_id, results[1].package_id)
        self.assertNotEqual(results[0].attempt_id, results[1].attempt_id)
