# 🏀 NBA MVP Predictor

A machine learning pipeline that predicts NBA MVP voting shares using 
player and team statistics. The model achieves 100% winner accuracy 
on out-of-sample test seasons (2024-2026).

🔗 **https://nba-mvp-predictor-bbndyzvuonzccegao6fceu.streamlit.app/**

---

## Overview
Brief 3-4 sentence description of the project, motivation, and result.

---

## Demo
Add a screenshot or GIF of your app here. This is the single most 
important thing — recruiters spend 30 seconds on a README.

---

## Methodology
- **Data Collection** — nba_api + Basketball Reference
- **Feature Engineering** — per game stats, season rank features
- **Modeling** — Ridge, Random Forest, XGBoost with temporal CV
- **Evaluation** — TimeSeriesSplit, out-of-sample test seasons

---

## Results
| Season | Predicted Winner | Actual Winner | Correct |
|--------|-----------------|---------------|---------|
| 2024   | Nikola Jokić    | Nikola Jokić  | ✅      |
| 2025   | SGA             | SGA           | ✅      |
| 2026   | SGA             | SGA           | ✅      |

---

## Project Structure
nba-mvp-predictor/
├── app/          # Streamlit application
├── data/         # processed datasets
├── models/       # trained model files
├── notebooks/    # analysis notebooks
└── src/          # reusable functions

---

## How to Run Locally
git clone https://github.com/matthewkilmer/nba-mvp-predictor.git
cd nba-mvp-predictor
pip install -r requirements.txt
streamlit run app/app.py

---

## Known Limitations & V2 Roadmap
- Advanced stats (BPM, VORP, WS) not yet included
- Live current season predictions coming in v2
- Two-stage model planned for improved zero-inflation handling

---

## Tech Stack
Python, XGBoost, scikit-learn, Streamlit, pandas, nba_api
