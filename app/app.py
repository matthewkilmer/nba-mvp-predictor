### THIS SCRIPT CONTAINS CODE TO CREATE AND LAUNCH STREAMLIT APPLICATION THAT VISUALIZES OUR RESULTS

# import libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from PIL import Image
import os
import requests
from io import BytesIO
from datetime import datetime

# page config - must be first streamlit command
st.set_page_config(
    page_title="NBA MVP Predictor",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# get app and root directory
APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(APP_DIR)

# load model and data
@st.cache_resource
def load_model():
    return joblib.load(os.path.join(ROOT_DIR, 'models', 'xgb_mvp_predictor.pkl'))

@st.cache_data
def load_data():
    return pd.read_csv(os.path.join(ROOT_DIR, 'data', 'processed', 'merged_df.csv'))

model = load_model()
df = load_data()

# make feature columns
features = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'MIN', 'GP',
                'FG_PCT', 'FG3_PCT', 'FT_PCT', 'PLUS_MINUS',
                'W_PCT', 'TEAM_W', 'PTS_RANK', 'AST_RANK',
                'REB_RANK', 'PLUS_MINUS_RANK', 'W_RANK']

# custom css for nba branding
st.markdown("""
    <style>
    /* main background */
    .stApp {
        background-color: #1a1a2e;
        color: white;
    }
    
    /* sidebar */
    [data-testid="stSidebar"] {
        background-color: #1D428A;
    }
    
    /* metric cards */
    [data-testid="stMetric"] {
        background-color: #16213e;
        border: 1px solid #C8102E;
        border-radius: 8px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# sidebar navigation
with st.sidebar:
    st.image("https://cdn.nba.com/logos/leagues/logo-nba.svg", width=100)
    st.title("NBA MVP Predictor")
    st.divider()
    
    page = st.radio(
        "Navigate",
        ["🔮 MVP Predictions", "📊 Model Insights", "📜 Historical Winners"],
        label_visibility="hidden"
    )

def get_historical_predictions(season):
    season_df = df[df['SEASON'] == season].copy()
    
    feature_cols = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'MIN', 'GP',
                    'FG_PCT', 'FG3_PCT', 'FT_PCT', 'PLUS_MINUS',
                    'W_PCT', 'TEAM_W', 'PTS_RANK', 'AST_RANK',
                    'REB_RANK', 'PLUS_MINUS_RANK', 'W_RANK']
    
    X = season_df[feature_cols]
    season_df['PREDICTED_SHARE'] = np.clip(model.predict(X), 0, 1)
    
    return season_df.nlargest(5, 'PREDICTED_SHARE')[
        ['PLAYER_NAME', 'PLAYER_ID', 'TEAM_ID', 'TEAM_NAME', 
         'PREDICTED_SHARE', 'MVP_SHARE']
    ].reset_index(drop=True)

def display_predictions(predictions, is_historical=True):
    
    # winner card at top
    winner = predictions.iloc[0]
    
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1D428A, #C8102E);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 24px;
        ">
            <div>
                <p style="color: #FFD700; font-size: 14px; margin: 0;">🏆 PREDICTED MVP</p>
                <h1 style="color: white; margin: 0;">{winner['PLAYER_NAME']}</h1>
                <p style="color: white; margin: 0;">{winner['TEAM_NAME']}</p>
                <p style="color: #FFD700; font-size: 24px; margin: 0;">
                    Predicted Share: {winner['PREDICTED_SHARE']:.3f}
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Top 5 MVP Candidates")
    st.divider()
    
    # one row per candidate
    for i, row in predictions.iterrows():
        col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 2])
        
        # rank
        with col1:
            st.markdown(f"### #{i+1}")
        
        # player headshot and name
        with col2:
            headshot_url = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{int(row['PLAYER_ID'])}.png"
            st.image(headshot_url, width=80)
            st.write(row['PLAYER_NAME'])
            st.caption(row['TEAM_NAME'])
        
        # predicted share bar
        with col3:
            st.metric("Predicted Share", f"{row['PREDICTED_SHARE']:.3f}")
            st.progress(float(row['PREDICTED_SHARE']))
        
        # actual share if historical
        with col4:
            if is_historical and row['MVP_SHARE'] > 0:
                st.metric("Actual Share", f"{row['MVP_SHARE']:.3f}")
                st.progress(float(row['MVP_SHARE']))
            elif is_historical:
                st.metric("Actual Share", "0.000")
        
        # accuracy indicator
        with col5:
            if is_historical:
                diff = abs(row['PREDICTED_SHARE'] - row['MVP_SHARE'])
                if diff < 0.1:
                    st.success("✅ Accurate")
                elif diff < 0.2:
                    st.warning("⚠️ Close")
                else:
                    st.error("❌ Off")
        
        st.divider()

def get_live_predictions():
    month = datetime.now().month
    if not (month >= 10 or month <= 6):
        return None

def is_season_active():
    month = datetime.now().month
    # NBA season runs roughly October through June
    return month >= 10 or month <= 6

def show_predictions():
    st.title("🔮 MVP Predictions")
    st.divider()
    
    # season selector
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # only show true out-of-sample test seasons
        TEST_SEASONS = [2024, 2025, 2026]

        season_options = ['Current Season (Live)'] + TEST_SEASONS[::-1]
        selected_season = st.selectbox("Select Season", season_options)

        st.info("📊 Historical predictions shown for 2024-2026 only (Predictions from 2000-2003 would be subject to data leakage!)")
    
    if selected_season == 'Current Season (Live)':
        predictions = get_live_predictions()
        if predictions is None:
            st.warning("🏀 Live predictions unavailable — NBA season hasn't started yet. Check back in October!")
            return  # stop execution here, don't call display_predictions
    else:
        predictions = get_historical_predictions(selected_season)
    
    display_predictions(predictions)

def show_feature_importance():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    importances = pd.Series(model.feature_importances_, index=features)
    importances.sort_values().plot(kind='barh', ax=ax, color='#1D428A')
    
    ax.set_title('XGBoost Feature Importances', color='white', fontsize=14)
    ax.set_facecolor('#1a1a2e')
    fig.patch.set_facecolor('#1a1a2e')
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    st.pyplot(fig)

def show_model_performance():
    
    # hardcode your results from the modeling notebook
    performance_data = {
        'Model': ['Ridge Regression', 'Random Forest', 'Random Forest (Tuned)', 
                  'XGBoost', 'XGBoost (Tuned)'],
        'RMSE': [0.0756, 0.0311, 0.0306, 0.0384, 0.0341],
        'R²': [0.2995, 0.8815, 0.8848, 0.8188, 0.8573],
        'Selected': ['', '', '', '', '✅']
    }
    
    perf_df = pd.DataFrame(performance_data)
    
    st.subheader("Model Comparison")
    st.caption("All models evaluated on out-of-sample test seasons 2024-2026")
    
    st.dataframe(
        perf_df,
        hide_index=True,
        use_container_width=True,
        column_config={
            'RMSE': st.column_config.NumberColumn(format="%.4f"),
            'R²': st.column_config.NumberColumn(format="%.4f"),
        }
    )
    
    # add three metric cards for the selected model
    st.subheader("Selected Model — XGBoost (Tuned)")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("RMSE", "0.0341", delta="-0.0415 vs baseline")
    with col2:
        st.metric("R²", "0.8573", delta="+0.5578 vs baseline")
    with col3:
        st.metric("Winner Accuracy", "3/3", delta="100% test seasons")

def show_predicted_vs_actual():
    
    # generate predictions for all test seasons
    test_df = df[df['SEASON'].isin([2024, 2025, 2026])].copy()
    X_test = test_df[features]
    test_df['PREDICTED_SHARE'] = np.clip(model.predict(X_test), 0, 1)
    
    # only plot vote getters for clarity
    plot_df = test_df[test_df['MVP_SHARE'] > 0].copy()
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    colors = {2024: '#1D428A', 2025: '#C8102E', 2026: '#FFD700'}
    
    for season in [2024, 2025, 2026]:
        season_data = plot_df[plot_df['SEASON'] == season]
        ax.scatter(
            season_data['MVP_SHARE'],
            season_data['PREDICTED_SHARE'],
            c=colors[season],
            label=str(season),
            s=100,
            alpha=0.8
        )
        
        # annotate each point with player last name
        for _, row in season_data.iterrows():
            ax.annotate(
                row['PLAYER_NAME'].split()[-1],
                (row['MVP_SHARE'], row['PREDICTED_SHARE']),
                textcoords='offset points',
                xytext=(8, 4),
                fontsize=8,
                color='white'
            )
    
    # perfect prediction line
    ax.plot([0, 1], [0, 1], 'w--', alpha=0.4, label='Perfect Prediction')
    
    ax.set_xlabel('Actual MVP Share', color='white')
    ax.set_ylabel('Predicted MVP Share', color='white')
    ax.set_title('Predicted vs Actual MVP Share (2024-2026)', color='white', fontsize=14)
    ax.legend(facecolor='#16213e', labelcolor='white')
    ax.set_facecolor('#1a1a2e')
    fig.patch.set_facecolor('#1a1a2e')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('white')
    
    st.pyplot(fig)
    st.caption("Only players who received MVP votes are shown. Points closer to the diagonal line indicate more accurate predictions.")

def show_insights():
    st.title("📊 Model Insights")
    st.divider()
    
    tab1, tab2, tab3 = st.tabs([ 
        "Model Performance", 
        "Predicted vs Actual",
        "Feature Importance"
    ])
    
    with tab1:
        show_model_performance()
    
    with tab2:
        show_predicted_vs_actual()
        
    with tab3:
        show_feature_importance()

def show_historical():
    st.title("📜 Historical MVP Winners")
    st.divider()
    
    # get the top share player for each season
    winners = df.loc[df.groupby('SEASON')['MVP_SHARE'].idxmax()].copy()
    winners = winners[winners['MVP_SHARE'] > 0].sort_values('SEASON')
    
    # winner bar chart
    fig, ax = plt.subplots(figsize=(16, 6))
    
    bars = ax.bar(winners['SEASON'], winners['MVP_SHARE'], 
                  color='#1D428A', edgecolor='#C8102E', linewidth=0.5)
    
    # highlight test seasons
    for i, row in winners.iterrows():
        if row['SEASON'] in [2024, 2025, 2026]:
            ax.bar(row['SEASON'], row['MVP_SHARE'], 
                   color='#C8102E', edgecolor='white', linewidth=0.5)
    
    # annotate with last names
    for _, row in winners.iterrows():
        ax.text(row['SEASON'], row['MVP_SHARE'] + 0.01,
                row['PLAYER_NAME'].split()[-1],
                ha='center', va='bottom', 
                fontsize=7, color='white', rotation=45)
    
    ax.set_title('NBA MVP Winner Share by Season (2000-2026)', 
                 color='white', fontsize=14)
    ax.set_xlabel('Season', color='white')
    ax.set_ylabel('MVP Share', color='white')
    ax.set_facecolor('#1a1a2e')
    fig.patch.set_facecolor('#1a1a2e')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('white')
    
    st.pyplot(fig)
    st.caption("🔴 Red bars indicate out-of-sample test seasons (2024-2026)")
    
    st.divider()
    
    # winner cards below chart
    st.subheader("All Time MVP Winners")
    
    # display in a clean table with headshots
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_winner = st.selectbox(
            "Select a season to view winner",
            sorted(winners['SEASON'].unique().tolist(), reverse=True)
        )
    
    winner_row = winners[winners['SEASON'] == selected_winner].iloc[0]
    
    col1, col2, col3 = st.columns([1, 2, 2])
    
    with col1:
        headshot_url = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{int(winner_row['PLAYER_ID'])}.png"
        st.image(headshot_url, width=120)
    
    with col2:
        st.metric("MVP Winner", winner_row['PLAYER_NAME'])
        st.metric("Team", winner_row['TEAM_NAME'])
    
    with col3:
        st.metric("MVP Share", f"{winner_row['MVP_SHARE']:.3f}")
        st.metric("Points Per Game", f"{winner_row['PTS']:.1f}")

# route to pages
if page == "🔮 MVP Predictions":
    show_predictions()
elif page == "📊 Model Insights":
    show_insights()
elif page == "📜 Historical Winners":
    show_historical()