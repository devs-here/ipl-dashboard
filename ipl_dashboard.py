import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="IPL Analysis Dashboard", page_icon="🏏", layout="wide")
st.title("🏏 IPL Analysis Dashboard (2008-2024)")
st.write("Analysis of IPL matches and deliveries data")

# Load data
@st.cache_data
def load_data():
    matches = pd.read_csv(r"D:\python\projects\matches.csv")
    deliveries = pd.read_csv(r"D:\python\projects\deliveries.csv")
    matches["city"] = matches["city"].fillna("Unknown")
    return matches, deliveries

matches, deliveries = load_data()

# ── 1. Most Wins by Team ──────────────────────────────────────────────────────
st.header("1. Most Wins by Team")
wins = matches["winner"].value_counts().reset_index()
wins.columns = ["teams", "wins"]

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=wins, x="wins", y="teams", ax=ax)
ax.set_title("Most Wins by Team in IPL History")
ax.set_xlabel("Wins")
ax.set_ylabel("Teams")
plt.tight_layout()
st.pyplot(fig)
plt.close()

# ── 2. Top 10 Run Scorers ─────────────────────────────────────────────────────
st.header("2. Top 10 Run Scorers")
top_scorers = deliveries.groupby("batter")["batsman_runs"].sum().reset_index()
top_scorers.columns = ["batter", "total_runs"]
top_scorers = top_scorers.sort_values("total_runs", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=top_scorers, x="total_runs", y="batter", ax=ax)
ax.set_title("Top 10 Run Scorers in IPL History")
ax.set_xlabel("Total Runs")
ax.set_ylabel("Batter")
plt.tight_layout()
st.pyplot(fig)
plt.close()

# ── 3. Top 10 Wicket Takers ───────────────────────────────────────────────────
st.header("3. Top 10 Wicket Takers")
wickets = deliveries[deliveries["is_wicket"] == 1]
top_wickets = wickets.groupby("bowler")["is_wicket"].sum().reset_index()
top_wickets.columns = ["bowler", "wickets"]
top_wickets = top_wickets.sort_values("wickets", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=top_wickets, x="wickets", y="bowler", ax=ax)
ax.set_title("Top 10 Wicket Takers in IPL History")
ax.set_xlabel("Wickets")
ax.set_ylabel("Bowler")
plt.tight_layout()
st.pyplot(fig)
plt.close()

# ── 4. Toss Decision ─────────────────────────────────────────────────────────
st.header("4. Toss Decision - Bat vs Field")
toss = matches["toss_decision"].value_counts().reset_index()
toss.columns = ["decision", "count"]

fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(toss["count"], labels=toss["decision"], autopct="%1.1f%%")
ax.set_title("Toss Decision - Bat vs Field")
plt.tight_layout()
st.pyplot(fig)
plt.close()

# ── 5. Most Player of the Match Awards ───────────────────────────────────────
st.header("5. Most Player of the Match Awards")
potm = matches["player_of_match"].value_counts().reset_index().head(10)
potm.columns = ["player", "awards"]

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=potm, x="awards", y="player", ax=ax)
ax.set_title("Most Player of the Match Awards")
ax.set_xlabel("Awards")
ax.set_ylabel("Player")
plt.tight_layout()
st.pyplot(fig)
plt.close()

# ── 6. Total Runs Per Season ──────────────────────────────────────────────────
st.header("6. Total Runs Scored Per Season")
season_runs = deliveries.merge(matches[["id", "season"]], left_on="match_id", right_on="id")
season_runs = season_runs.groupby("season")["total_runs"].sum().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=season_runs, x="season", y="total_runs", ax=ax)
ax.set_title("Total Runs Scored Per Season")
ax.set_xlabel("Season")
ax.set_ylabel("Total Runs")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)
plt.close()

# ── 7. Top 10 Venues ────────────────────────────────────────────────────────
st.header("7. Top 10 Venues by Matches Hosted")
venue = matches["venue"].value_counts().reset_index().head(10)
venue.columns = ["venue", "matches"]

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=venue, x="matches", y="venue", ax=ax)
ax.set_title("Top 10 Venues by Matches Hosted")
ax.set_xlabel("Matches")
ax.set_ylabel("Venue")
plt.tight_layout()
st.pyplot(fig)
plt.close()

# ── 8. Runs vs Boundaries (Scatter) ──────────────────────────────────────────
st.header("8. Runs vs Boundaries per Batter")
runs = deliveries.groupby("batter")["batsman_runs"].sum().reset_index()
runs.columns = ["batter", "total_runs"]
bounds = deliveries[deliveries["batsman_runs"].isin([4, 6])].groupby("batter")["batsman_runs"].count().reset_index()
bounds.columns = ["batter", "boundaries"]
scatter_df = runs.merge(bounds, on="batter")

fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=scatter_df, x="total_runs", y="boundaries", ax=ax)
ax.set_title("Runs vs Boundaries per Batter")
ax.set_xlabel("Total Runs")
ax.set_ylabel("Boundaries")
plt.tight_layout()
st.pyplot(fig)
plt.close()

# ── 9. Top 10 Boundary Hitters ───────────────────────────────────────────────
st.header("9. Top 10 Boundary Hitters")
boundaries = deliveries[deliveries["batsman_runs"].isin([4, 6])]
top_boundaries = boundaries.groupby("batter")["batsman_runs"].count().reset_index()
top_boundaries.columns = ["batter", "boundaries"]
top_boundaries = top_boundaries.sort_values("boundaries", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=top_boundaries, x="boundaries", y="batter", ax=ax)
ax.set_title("Top 10 Boundary Hitters in IPL History")
ax.set_xlabel("Boundaries")
ax.set_ylabel("Batter")
plt.tight_layout()
st.pyplot(fig)
plt.close()

# ── 10. Highest Team Total in a Single Innings ───────────────────────────────
st.header("10. Highest Team Total in a Single Innings")
team_totals = deliveries.groupby(["match_id", "batting_team"])["total_runs"].sum().reset_index()
team_totals = team_totals.sort_values("total_runs", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=team_totals, x="total_runs", y="batting_team", ax=ax)
ax.set_title("Highest Team Total in a Single Innings")
ax.set_xlabel("Total Runs")
ax.set_ylabel("Team")
plt.tight_layout()
st.pyplot(fig)
plt.close()

# ── 11. Team Wins Per Season (Heatmap) ───────────────────────────────────────
st.header("11. Team Wins Per Season")
pivot = matches.groupby(["winner", "season"]).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(14, 6))
sns.heatmap(pivot, annot=True, fmt="d", cmap="Blues", ax=ax)
ax.set_title("Team Wins Per Season")
ax.set_xlabel("Season")
ax.set_ylabel("Team")
plt.tight_layout()
st.pyplot(fig)
plt.close()
