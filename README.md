[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18665489.svg)](https://doi.org/10.5281/zenodo.18665489)

# Noisy IPD Dynamics

**Noise-Induced Regime Transitions in the Iterated Prisoner’s Dilemma**  
A computational study of strategy robustness under stochastic signal corruption.

📄 Preprint available on Zenodo: https://doi.org/10.5281/zenodo.18665489

---

## Overview

This repository contains a large-scale simulation framework for studying strategic performance in the Iterated Prisoner’s Dilemma (IPD) under increasing stochastic noise.

The project investigates how signal corruption affects:

- Cooperative stability  
- Strategic dominance  
- Variance and regime transitions  
- Adaptive robustness under uncertainty  

Noise levels are systematically varied from **0% to 50%**, and performance is evaluated across multiple independent seeds using parallelized simulation.

Results reveal distinct behavioral regimes:

- **Low noise:** Cooperative reciprocators dominate  
- **Intermediate noise:** Retaliatory instability increases variance  
- **High noise:** Defection-dominant strategies prevail  
- **Adaptive strategies:** Exhibit structural robustness in transitional regimes  

---

## Research Contribution

This project provides:

- A reproducible computational framework for IPD tournaments  
- Systematic mapping of noise-induced regime transitions  
- Statistical evaluation across 100 independent seeds  
- 95% confidence interval estimation for performance metrics  
- Parallelized experiment execution for scalability  
- An adaptive profitability-based strategy evaluated against canonical benchmarks  

---

## Repository Structure

```
.
├── engine.py              # Core Iterated Prisoner's Dilemma implementation
├── strategies.py          # Strategy definitions
├── tournament.py          # Round-robin tournament logic
├── main.py                # Single tournament execution
├── experiments.py         # Parallelized multi-seed noise experiments
└── README.md
```

---

## Model Description

### Stage Game

Payoff matrix:

|        | C      | D      |
|--------|--------|--------|
| **C**  | (3,3)  | (0,5)  |
| **D**  | (5,0)  | (1,1)  |

With ordering:

- T > R > P > S  
- 2R > T + S  

---

### Noise Model

Let ε ∈ [0,1] denote the corruption probability.

Each intended action is flipped with probability ε:

- With probability (1 − ε): action executed as intended  
- With probability ε: action is inverted  

Noise levels evaluated:

```
[0.00, 0.05, 0.10, ..., 0.50]
```

---

## Strategies Included

- Always Cooperate (AC)  
- Always Defect (AD)  
- Tit-for-Tat (TFT)  
- Tit-for-Tat (Defect-First)  
- Generous Tit-for-Tat (GTFT)  
- Two-Tits-for-Tat (2TFT)  
- Grim Trigger (GT)  
- Random Strategy (RS)  
- Win-Stay Lose-Shift (WSLS)  
- Majority Strategy (MS)  
- Profitability-Adaptive Strategy (PAS)  

---

## Experimental Setup

- Rounds per match: 10,000  
- Seeds per noise level: 100  
- Full round-robin including self-play  
- Parallelized execution using multiprocessing  
- Mean payoff per round reported  
- 95% confidence intervals computed as:

```
mean ± 1.96 * (std / sqrt(N))
```

---

## Running the Code

### Single Tournament

```
python main.py
```

### Full Parallel Experiment (All Noise Levels)

```
python experiments.py
```

You can modify experimental parameters directly inside `experiments.py`:

- `ROUNDS`
- `NUM_SEEDS`
- `NOISE_VALUES`
- `NUM_PROCESSES`

---

## Key Findings (Summary)

- Cooperative strategies dominate under low corruption.
- Intermediate noise induces retaliatory cascades and elevated variance.
- Beyond a critical corruption threshold (~0.25–0.35), defection becomes dominant.
- The Profitability-Adaptive Strategy maintains competitive rank stability across moderate and high noise regimes.

---

## Reproducibility

All simulations are deterministic given:

- Fixed random seed  
- Fixed noise parameter  
- Fixed strategy set  

Parallel execution preserves seed isolation.

---

## Future Extensions

- Evolutionary dynamics (replicator updates)  
- Analytical approximation of regime thresholds  
- Reinforcement learning variants  
- Alternative noise models (perception vs implementation error)  
- Asymmetric payoff matrices  

---

## Author

Alan Jacob  

For academic correspondence, see preprint:  
https://doi.org/10.5281/zenodo.18665489

---

## Citation

If you use this work, please cite:

Jacob, A. (2026). *Noise-Induced Regime Transitions in the Iterated Prisoner's Dilemma: A Computational Study of Strategy Robustness*. Zenodo. https://doi.org/10.5281/zenodo.18665489

---

## License

This repository contains both software and associated research materials.

---

### Code License

The source code in this repository is licensed under the **MIT License**.

Copyright (c) 2026 Alan Jacob

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

---

### Research Paper License

The accompanying research article:

> *Noise-Induced Regime Transitions in the Iterated Prisoner’s Dilemma:  
> A Computational Study of Strategy Robustness*

is licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

This permits sharing and adaptation for any purpose, including commercial use,
provided appropriate credit is given.

Zenodo DOI:  
https://doi.org/10.5281/zenodo.18665489
