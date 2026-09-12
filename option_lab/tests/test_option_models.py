import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from option_models import Option, finite_difference_delta, monte_carlo_price, simulate_short_call_hedge


class OptionModelTests(unittest.TestCase):
    def setUp(self):
        self.call = Option(spot=100, strike=100, rate=0.05, volatility=0.2, maturity=1, kind="call")
        self.put = Option(spot=100, strike=100, rate=0.05, volatility=0.2, maturity=1, kind="put")

    def test_put_call_parity(self):
        self.assertAlmostEqual(self.call.price() - self.put.price(), 100 - 100 * __import__("math").exp(-0.05), places=8)

    def test_finite_difference_delta(self):
        self.assertAlmostEqual(self.call.delta(), finite_difference_delta(self.call), places=4)

    def test_monte_carlo_converges_near_closed_form(self):
        estimate, error = monte_carlo_price(self.call, paths=80_000, seed=1)
        self.assertLess(abs(estimate - self.call.price()), 4 * error)

    def test_hedging_returns_a_path_distribution(self):
        pnl = simulate_short_call_hedge(self.call, realised_volatility=0.2, paths=500, steps=32, seed=1)
        self.assertEqual(len(pnl), 500)
        self.assertTrue(__import__("numpy").isfinite(pnl).all())


if __name__ == "__main__":
    unittest.main()
