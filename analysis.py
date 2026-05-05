import pandas as pd

def load_data():
    """Load the IPL ball-by-ball CSV file"""
    df = pd.read_csv("data/IPL.csv")
    return df

def get_match_level(df):
    """
    Convert ball-by-ball data to match-level data.
    Each match_id becomes one row with key match info.
    """
    match_df = df.drop_duplicates(subset=["match_id"]).copy()
    return match_df

def clean_data(df):
    """Remove bad rows and fix data types"""
    # Drop rows where match result is missing
    df = df.dropna(subset=["match_won_by"])

    # Convert season to integer
    df["season"] = df["season"].astype(str).str[:4].astype(int)

    # Strip extra spaces
    df["match_won_by"] = df["match_won_by"].str.strip()
    df["batting_team"] = df["batting_team"].str.strip()
    df["bowling_team"] = df["bowling_team"].str.strip()

    return df

def team_wins(match_df):
    """Count wins per team"""
    wins = match_df["match_won_by"].value_counts().reset_index()
    wins.columns = ["team", "wins"]
    # Remove non-team values like 'No Result'
    wins = wins[~wins["team"].isin(["No Result", "Tied", "N/A"])]
    return wins

def toss_decision(match_df):
    """How often teams chose bat vs field"""
    toss = match_df["toss_decision"].value_counts().reset_index()
    toss.columns = ["decision", "count"]
    return toss

def wins_per_season(match_df):
    """Total matches played per season"""
    season = match_df.groupby("season")["match_id"].count().reset_index()
    season.columns = ["season", "matches"]
    return season

def top_venues(match_df):
    """Top 10 venues by matches hosted"""
    venues = match_df["venue"].value_counts().head(10).reset_index()
    venues.columns = ["venue", "matches"]
    return venues

def toss_match_winner(match_df):
    """Did winning toss help win the match?"""
    df = match_df.copy()
    df["toss_helped"] = df["toss_winner"] == df["match_won_by"]
    return df["toss_helped"].value_counts()

def player_of_match_awards(match_df):
    """Top 10 players with most Player of the Match awards"""
    top = match_df["player_of_match"].value_counts().head(10).reset_index()
    top.columns = ["player", "awards"]
    return top

def head_to_head(match_df):
    """Team vs team win matrix"""
    h2h = pd.crosstab(match_df["match_won_by"], match_df["batting_team"])
    return h2h

def top_run_scorers(df):
    """Top 10 run scorers across all IPL using ball-by-ball data"""
    runs = df.groupby("batter")["runs_batter"].sum().reset_index()
    runs.columns = ["batter", "total_runs"]
    runs = runs.sort_values("total_runs", ascending=False).head(10)
    return runs

def top_wicket_takers(df):
    """Top 10 wicket takers using ball-by-ball data"""
    # Only count actual wickets, exclude run outs
    wickets = df[
        df["wicket_kind"].notna() &
        ~df["wicket_kind"].isin(["run out", "obstructing the field"])
    ]
    wkt = wickets.groupby("bowler")["wicket_kind"].count().reset_index()
    wkt.columns = ["bowler", "wickets"]
    wkt = wkt.sort_values("wickets", ascending=False).head(10)
    return wkt
