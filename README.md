# Multi-Market Algorithmic Trading Strategies

## 📌 Overview
This repository contains two complete algorithmic trading systems developed and tested across six global markets (forex and crypto). The goal was to create a risk-managed framework capable of generating consistent monthly returns while keeping drawdown tightly controlled.

### ✅ Strategy 1: Momentum (Candle-based)
- Triggered by price action momentum (e.g., consecutive bullish/bearish candles)
- SL/TP dynamically scaled based on candle structure
- Tested on BTCUSD, ETHUSD, and EURUSD

### ✅ Strategy 2: Hilega Milega (Indicator-based)
- Based on crossover signals using Hilega Milega indicator + RSI filters
- Trailing stop logic built into the system
- Tested on AUDUSD, AUDCAD, and USDJPY

## 📈 Results Summary
- **Avg Monthly Return**: ~4.16%
- **Max Drawdown**: ≤10%
- **Markets Tested**: BTCUSD, ETHUSD, EURUSD, AUDCAD, AUDUSD, USDJPY
- **Prop Firm Challenge**: Successfully passed (13% profit in under 3 months)

## 📂 Repository Structure

.
├── strategies/
│ ├── momentum/
│ │ ├── strategy_1_momentum.py
│ │ └── output1.csv
│ ├── hm/
│ │ ├── strategy_2_hilega_milega.py
│ │ └── output2.csv
├── utils/
│ ├── momentum/
│ │ └── maxloss_momentum.py
│ ├── hm/
│ │ └── maxloss_hm.py
├── results/
│ └── [performance snapshots, trade logs, screenshots]
└── README.md


## 🧠 Key Features
- Multi-market execution with normalized `x` scaling logic
- SL/TP optimization through variable-based segmentation
- Drawdown computation from every possible start-date
- Strategy-layered portfolio allocation
- Real-world backtests, not just theoretical models

## 📢 Notes
- The project was built iteratively over a year, combining manual backtesting, code-based simulations, and live trading validation.
- Code is not beginner-friendly by design — it’s real-world quant logic, not a tutorial.
- All strategy logic and supporting files are publicly shared for credibility and transparency.

## 📜 License
MIT License — free to use, adapt, and modify with attribution.

---

**For the full story behind how this project was built and validated, check out my [LinkedIn article](#)** (https://www.linkedin.com/posts/swapnil-phutane-64100129a_from-raw-ideas-to-code-testing-optimization-activity-7343247964938653698-MHhO?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEhCalEBSXurViZCpRx8NIRefuIxDnAAucI).
