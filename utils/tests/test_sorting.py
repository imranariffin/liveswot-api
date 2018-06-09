from django.test import TestCase
from ..sorting import confidence


class TestSortingUtils(TestCase):
    def test_confidence_should_return_correct_values(self):
        ups_and_downs = [
            (1, 0),
            (40, 20),
            (10, 0),
            (100, 80),
            (10, 20),
            (5, 0),
            (0, 1),
            (0, 100),
        ]

        expected_returns = [
            0.3784475,
            0.5851513,
            0.8589313,
            0.5078007,
            0.2342384,
            0.7527428,
            0,
            0,
        ]

        for i in range(len(ups_and_downs)):
            ups, downs = ups_and_downs[i]
            expected = expected_returns[i]

            self.assertAlmostEqual(expected, confidence(ups, downs), delta=0.0000001)