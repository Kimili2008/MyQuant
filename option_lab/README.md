# Option Pricing and Hedging Lab

This lab implements European option pricing, analytical Greeks, finite-difference validation, Monte Carlo pricing, and discrete delta hedging. It is a numerical-risk exercise, not a trading system.

## Run

```bash
python3 -m unittest discover -s tests -v
python3 src/run_lab.py
```

The run writes a compact CSV summary into `results/`.

## Questions to answer in interview

- Why does a call's value rise with volatility?
- What assumptions does Black-Scholes make?
- Why can a delta hedge lose money even when the pricing formula is correct?
- How do daily and weekly rebalancing differ when realised volatility differs from implied volatility?
