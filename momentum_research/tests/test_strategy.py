import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from strategy import performance_metrics, portfolio_returns, rebalance_weights, twelve_one_signal


class StrategyTests(unittest.TestCase):
    def setUp(self):
        index = pd.bdate_range("2020-01-01", periods=320)
        self.prices = pd.DataFrame({
            "SPY": 100 * np.cumprod(1 + np.full(len(index), 0.0003)),
            "AAA": 100 * np.cumprod(1 + np.full(len(index), 0.0005)),
            "BBB": 100 * np.cumprod(1 + np.full(len(index), 0.0001)),
        }, index=index)

    def test_signal_excludes_recent_month(self):
        signal = twelve_one_signal(self.prices, lookback=252, skip=21)
        expected = self.prices["AAA"].iloc[-22] / self.prices["AAA"].iloc[-253] - 1
        self.assertAlmostEqual(signal["AAA"].iloc[-1], expected)

    def test_weights_sum_to_zero_or_one(self):
        weights = rebalance_weights(self.prices, "momentum_inverse_vol", top_n=2)
        sums = weights.sum(axis=1)
        self.assertTrue(((sums.round(10) == 0.0) | (sums.round(10) == 1.0)).all())

    def test_costs_reduce_return_when_turnover_exists(self):
        weights = rebalance_weights(self.prices, "momentum_equal", top_n=1)
        zero_cost, turnover = portfolio_returns(self.prices, weights, 0.0)
        with_cost, _ = portfolio_returns(self.prices, weights, 10.0)
        self.assertLessEqual(with_cost.sum(), zero_cost.sum())
        self.assertGreater(turnover.sum(), 0.0)

    def test_metrics_include_drawdown(self):
        returns = pd.Series([0.1, -0.2, 0.1])
        turnover = pd.Series([1.0, 0.0, 0.0])
        metrics = performance_metrics(returns, turnover)
        self.assertLess(metrics["max_drawdown"], 0.0)


if __name__ == "__main__":
    unittest.main()
