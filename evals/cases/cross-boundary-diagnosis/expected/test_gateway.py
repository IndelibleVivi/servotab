import unittest
from gateway import admit
from probe import run


class GatewayTests(unittest.TestCase):
    def test_admission_ownership(self):
        for origin in ("local", "client"):
            for active in (False, True):
                for tag in (False, True):
                    for slot in (1, 4, 5, 8):
                        with self.subTest(origin=origin, active=active, tag=tag, slot=slot):
                            expected = origin == "local" or (active and tag) or slot <= 4
                            self.assertEqual(admit(origin=origin, relay_active=active,
                                                   relay_tag=tag, slot=slot), expected)

    def test_delivery_and_residual_delay(self):
        clean = run(origin="client", requests=8)
        noisy = run(origin="client", requests=8, access="noisy")
        self.assertEqual((clean["admission_dropped"], clean["delivered"],
                          clean["within_deadline"]), (0, 8, 8))
        self.assertEqual((noisy["admission_dropped"], noisy["delivered"],
                          noisy["within_deadline"]), (0, 8, 4))


if __name__ == "__main__":
    unittest.main()
