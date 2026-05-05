import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from analysis import (
    load_data, get_match_level, clean_data,
    team_wins, toss_decision, wins_per_season,
    top_venues, toss_match_winner, player_of_match_awards,
    head_to_head, top_run_scorers, top_wicket_takers
)

# ── Page setup ────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Dashboard 🏏",
    page_icon="🏏",
    layout="wide"
)

# ── Header ────────────────────────────────────────────────
st.title("IPL Data Dashboard")
st.caption("Analysing IPL matches from 2008–2025 using Python & pandas")
st.divider()

# ── Load data ─────────────────────────────────────────────
@st.cache_data
def get_data():
    df = load_data()
    df = clean_data(df)
    match_df = get_match_level(df)
    return df, match_df

df, match_df = get_data()

# ── Sidebar filters ───────────────────────────────────────
st.sidebar.title("Filters")
seasons = sorted(match_df["season"].unique())
selected_season = st.sidebar.selectbox(
    "Select Season", ["All Seasons"] + list(seasons)
)

all_teams = sorted(match_df["batting_team"].unique())
selected_team = st.sidebar.selectbox(
    "Select Team", ["All Teams"] + list(all_teams)
)

# Apply filters
filtered_match = match_df.copy()
filtered_ball = df.copy()

if selected_season != "All Seasons":
    filtered_match = filtered_match[filtered_match["season"] == selected_season]
    filtered_ball = filtered_ball[filtered_ball["season"] == selected_season]

if selected_team != "All Teams":
    filtered_match = filtered_match[
        (filtered_match["batting_team"] == selected_team) |
        (filtered_match["bowling_team"] == selected_team)
    ]
    filtered_ball = filtered_ball[
        (filtered_ball["batting_team"] == selected_team) |
        (filtered_ball["bowling_team"] == selected_team)
    ]

# ── Metric cards ──────────────────────────────────────────
st.subheader("Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Matches", filtered_match["match_id"].nunique())
col2.metric("Seasons", filtered_match["season"].nunique())
col3.metric("Teams", filtered_match["batting_team"].nunique())
col4.metric("Venues", filtered_match["venue"].nunique())
st.divider()

# ── Chart 1: Team wins ────────────────────────────────────
st.subheader("Most Wins by Team")
wins = team_wins(filtered_match)

fig1, ax1 = plt.subplots(figsize=(10, 5))
bars = ax1.barh(wins["team"], wins["wins"], color="steelblue")
ax1.bar_label(bars, padding=3)
ax1.set_xlabel("Number of Wins")
ax1.set_title("IPL Wins by Team")
ax1.invert_yaxis()
plt.tight_layout()
st.pyplot(fig1)
plt.close()
st.divider()

# ── Chart 2: Toss decision + effect ──────────────────────
st.subheader("Toss Decision — Bat or Field?")
col_a, col_b = st.columns([1, 2])

with col_a:
    toss = toss_decision(filtered_match)
    fig2, ax2 = plt.subplots(figsize=(4, 4))
    ax2.pie(
        toss["count"],
        labels=toss["decision"],
        autopct="%1.1f%%",
        startangle=90,
        colors=["#4CAF50", "#2196F3"]
    )
    ax2.set_title("Toss Decision")
    st.pyplot(fig2)
    plt.close()

with col_b:
    st.write("### Did Winning Toss Help?")
    toss_effect = toss_match_winner(filtered_match)
    fig3, ax3 = plt.subplots(figsize=(5, 4))
    ax3.bar(
        ["Toss Winner Won", "Toss Winner Lost"],
        toss_effect.values,
        color=["#4CAF50", "#f44336"]
    )
    ax3.set_ylabel("Number of Matches")
    ax3.set_title("Toss Effect on Match Result")
    st.pyplot(fig3)
    plt.close()

st.divider()

# ── Chart 3: Matches per season ───────────────────────────
st.subheader("Matches Played Per Season")
season_data = wins_per_season(filtered_match)

fig4, ax4 = plt.subplots(figsize=(12, 4))
ax4.plot(
    season_data["season"],
    season_data["matches"],
    marker="o",
    color="darkorange",
    linewidth=2,
    markersize=7
)
ax4.fill_between(
    season_data["season"],
    season_data["matches"],
    alpha=0.2,
    color="darkorange"
)
ax4.set_xlabel("Season")
ax4.set_ylabel("Matches")
ax4.set_title("IPL Matches Per Season")
ax4.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig4)
plt.close()
st.divider()

# ── Chart 4: Top venues ───────────────────────────────────
st.subheader("Top 10 Venues by Matches Hosted")
venues = top_venues(filtered_match)

fig5, ax5 = plt.subplots(figsize=(10, 5))
bars2 = ax5.barh(venues["venue"], venues["matches"], color="mediumseagreen")
ax5.bar_label(bars2, padding=3)
ax5.set_xlabel("Number of Matches")
ax5.set_title("Top Venues")
ax5.invert_yaxis()
plt.tight_layout()
st.pyplot(fig5)
plt.close()
st.divider()

# ── Chart 5: Player of the match ──────────────────────────
st.subheader("Top 10 Player of the Match Awards")
top_players = player_of_match_awards(filtered_match)

fig6, ax6 = plt.subplots(figsize=(10, 5))
bars3 = ax6.barh(top_players["player"], top_players["awards"], color="mediumpurple")
ax6.bar_label(bars3, padding=3)
ax6.set_xlabel("Awards")
ax6.set_title("Most Player of the Match Awards")
ax6.invert_yaxis()
plt.tight_layout()
st.pyplot(fig6)
plt.close()
st.divider()

# ── Chart 6: Top run scorers ──────────────────────────────
st.subheader("Top 10 Run Scorers")
top_runs = top_run_scorers(filtered_ball)

fig7, ax7 = plt.subplots(figsize=(10, 5))
bars4 = ax7.barh(top_runs["batter"], top_runs["total_runs"], color="tomato")
ax7.bar_label(bars4, padding=3)
ax7.set_xlabel("Total Runs")
ax7.set_title("Top Run Scorers in IPL")
ax7.invert_yaxis()
plt.tight_layout()
st.pyplot(fig7)
plt.close()
st.divider()

# ── Chart 7: Top wicket takers ────────────────────────────
st.subheader("Top 10 Wicket Takers")
top_wkts = top_wicket_takers(filtered_ball)

fig8, ax8 = plt.subplots(figsize=(10, 5))
bars5 = ax8.barh(top_wkts["bowler"], top_wkts["wickets"], color="steelblue")
ax8.bar_label(bars5, padding=3)
ax8.set_xlabel("Total Wickets")
ax8.set_title("Top Wicket Takers in IPL")
ax8.invert_yaxis()
plt.tight_layout()
st.pyplot(fig8)
plt.close()
st.divider()

# ── Chart 8: Heatmap ──────────────────────────────────────
st.subheader("Head-to-Head Wins Heatmap")
st.caption("Row = winning team | Column = opponent team")

h2h = head_to_head(filtered_match)
fig9, ax9 = plt.subplots(figsize=(14, 8))
sns.heatmap(
    h2h,
    annot=True,
    fmt="d",
    cmap="YlOrRd",
    ax=ax9,
    linewidths=0.5
)
ax9.set_title("Head to Head Wins")
plt.tight_layout()
st.pyplot(fig9)
plt.close()
st.divider()

# ── Raw data viewer ───────────────────────────────────────
with st.expander(" View Raw Match Data"):
    st.dataframe(filtered_match, use_container_width=True)

st.caption("Built by Baby Shalini · Data from Kaggle · Powered by Streamlit")