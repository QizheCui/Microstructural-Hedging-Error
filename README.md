# Microstructural Hedging Error

This project is based on the paper "On the Microstructural Hedging Error" by Christian Y. Robert and Mathieu Rosenbaum. We have implemented the hedging strategy presented in the paper and improved the strategy with more flexible settings discussed below.

## Overview

- **UctZone.py**: This file implement the uncertainty zone model with various flexible setting, with functions to
  - Generate the efficient price using Black-Scholes GBM or CEV model

  - Calculate exit time using fixed jump size or a naive random jump size

  - Generate the observed price with three jump time modes available

  - Plotting with various choices of detail included

- **Hedging_error.ipynb**: This notebook contains a detailed implementation of the uncertainty zone model, benchmark hedging strategy, and demonstrates the hedging errors under the uncertainty zone model without noise ($L_1$), with noise hedge for every tick ($L_2$), and with noise hedge for optimal tick ($L_3$).

- **MonteCarlo.ipynb**: This notebook simulates the hedging errors $L_1$, $L_2$, $L_3$ with either 1000 or 100 simulations. Note that we only include the simulation for the original paper in the notebook for reference $\eta=0.05$, $\sigma=0.01$, $\alpha = 0.05$. But by simply changing the parameter in **UctZone.py**, we can easily botain the following scenarios:
  - Fixed $L = 1$ vs. random $L$ with `np.random.choice([1,2,3],[0.7,0.2,0.1])`
  - Different volatility: $\sigma = 0.01$ vs. $\sigma = 0.01$
  - Different price aversion: $\eta = 0.05, 0.01, 0.5, 0.8$
  - Constant Volatility vs. Local Volatility (CEV model) with different $\beta = 0.8, 0.5$

The simulation results are all saved under the Simulation_Results folder.

## Contributors

- Ethan Qizhe Cui (CID: 01954652)
- Kelvin Wu (CID: 01955564)
- Ahmed Reda Seghrouchni (CID: 02278403)