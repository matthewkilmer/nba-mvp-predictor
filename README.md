# 🏀 NBA MVP Predictor

A machine learning pipeline that predicts NBA MVP voting shares using 
player and team statistics. The model achieves 100% winner accuracy 
on out-of-sample test seasons (2024-2026).

🔗 **https://nba-mvp-predictor-bbndyzvuonzccegao6fceu.streamlit.app/**

---

## Overview
The purpose of this project was to train a machine learning model to accurate predict the MVP share of NBA players over a given season. While the model was trained and tested on seasons that have already concluded, the utility of this model comes from the prospect of being able to continuously update MVP predictions throughout an NBA season, before the winners are chosen. This project includes data collection, cleaning & preprocessing, as well as the production of mulitple machine learning models. From there, a candidate model was chosen to make predictions seen in the streamlit app above.

---

## Demo
<img width="1900" height="912" alt="image" src="https://github.com/user-attachments/assets/74f1900d-5b25-4568-96f1-586df73fbf9e" />

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
