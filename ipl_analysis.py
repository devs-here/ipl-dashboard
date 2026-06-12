import pandas as pd

matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

print("MATCHES SHAPE:", matches.shape)
print("MATCHES COLUMNS:", matches.columns.tolist())
print(matches.head())

print("---")

print("DELIVERIES SHAPE:", deliveries.shape)
print("DELIVERIES COLUMNS:", deliveries.columns.tolist())
print(deliveries.head())

print(matches.isnull().sum())
print("---")
print(deliveries.isnull().sum())

matches['city'] = matches["city"].fillna("Unknown")

print(matches.isnull().sum())

# most wins by teams
wins = matches["winner"].value_counts().reset_index()
wins.columns = ["teams", "wins"]
print(wins)


import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize = (12,6))
sns.barplot(data=wins, x="wins", y="teams")
plt.title("Most wins by team in IPL history")
plt.xlabel("Wins")
plt.ylabel("Teams")
plt.tight_layout()
plt.show()

# top_scorers
top_scorers = deliveries.groupby("batter")["batsman_runs"].sum().reset_index()
top_scorers.columns = ["batter", "total_runs"]
top_scorers = top_scorers.sort_values("total_runs", ascending=False).head(10)
print(top_scorers)

plt.figure(figsize=(12,6))
sns.barplot(data=top_scorers, x="total_runs", y="batter")
plt.title("Top 10 run scorers in IPL history")
plt.xlabel("Total Runs")
plt.ylabel("Batter")
plt.tight_layout()
plt.show()

# Most Wicket Taker
wickets = deliveries[deliveries["is_wicket"] ==1]

top_wickets = wickets.groupby("bowler")["is_wicket"].sum().reset_index()
top_wickets.columns = ["bowler", "wickets"]
top_wickets = top_wickets.sort_values("wickets", ascending=False).head(10)


plt.figure(figsize=(12,6))
sns.barplot(data= top_wickets, x="wickets", y="bowler")
plt.title("Top 10 wicket takers in IPL history")
plt.xlabel("Wickets")
plt.ylabel("Bowlers")
plt.tight_layout()
plt.show()

# Toss
toss = matches["toss_decision"].value_counts().reset_index()
toss.columns = ["decision", "count"]
print(toss)

plt.figure(figsize=(6,6))
plt.pie(toss["count"], labels=toss["decision"], autopct="%1.1f%%")
plt.title("Toss decision - bat vs field")
plt.show()

# Most "player of the match"

potm = matches["player_of_match"].value_counts().reset_index().head(10)
potm.columns = ["player", "awards"]
print(potm)

plt.figure(figsize=(12,6))
sns.barplot(data=potm, x="awards", y="player")
plt.title("Most Player of the Match awards")
plt.xlabel("Awards")
plt.ylabel("Player")
plt.tight_layout()
plt.show()

# Total runs scored per season

season_runs = deliveries.merge(matches[["id", "season"]], left_on="match_id", right_on="id")
season_runs = season_runs.groupby("season")["total_runs"].sum().reset_index()
print(season_runs)

plt.figure(figsize=(12,6))
sns.barplot(data=season_runs, x="season", y="total_runs")
plt.title("Total runs scored per season")
plt.xlabel("Season")
plt.ylabel("Total Runs")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#  Best Venue

venue = matches["venue"].value_counts().reset_index().head(10)
venue.columns = ["venue", "matches"]
print(venue)

plt.figure(figsize=(12,6))
sns.barplot(data=venue, x="matches", y="venue")
plt.title("Top 10 venues by matches hosted")
plt.xlabel("Matches")
plt.ylabel("Venue")
plt.tight_layout()
plt.show()


# runs vs Boundaries

#total runs per batter
runs = deliveries.groupby("batter")["batsman_runs"].sum().reset_index()
runs.columns = ["batter", "total_runs"]

#total boundaries per batter
bounds = deliveries[deliveries["batsman_runs"].isin([4,6])].groupby("batter")["batsman_runs"].count().reset_index()
bounds.columns = ["batter", "boundaries"]

#merge 
scatter_df = runs.merge(bounds, on="batter")

plt.figure(figsize=(10,6))
sns.scatterplot(data=scatter_df, x="total_runs", y="boundaries")
plt.title("Runs vs Boundaries per person")
plt.xlabel("Total Runs")
plt.ylabel("Boundaries")
plt.tight_layout()
plt.show()

# top hitters
boundaries = deliveries[deliveries["batsman_runs"].isin([4,6])]
top_boundaries = boundaries.groupby("batter")["batsman_runs"].count().reset_index()
top_boundaries.columns = ["batter", "boundaries"]
top_boundaries = top_boundaries.sort_values("boundaries", ascending=False).head(10)
print(top_boundaries)

plt.figure(figsize=(12,6))
sns.barplot(data=top_boundaries, x="boundaries", y="batter")
plt.title("Top 10 boundary hitters in IPL history")
plt.xlabel("Boundaries")
plt.ylabel("Batter")
plt.tight_layout()
plt.show()

# Highest team total in a single innings

team_totals = deliveries.groupby(["match_id", "batting_team"])["total_runs"].sum().reset_index()
team_totals = team_totals.sort_values("total_runs", ascending=False).head(10)
print(team_totals)

plt.figure(figsize=(12,6))
sns.barplot(data=team_totals, x="total_runs", y="batting_team")
plt.title("Highest team total in a single innings")
plt.xlabel("Total Runs")
plt.ylabel("Team")
plt.tight_layout()
plt.show()

# Teams wins per season
pivot = matches.groupby(["winner", "season"]).size().unstack(fill_value=0)

plt.figure(figsize=(14,6))
sns.heatmap(pivot, annot=True, fmt="d", cmap="Blues")
plt.title("Team wins per season")
plt.xlabel("Season")
plt.ylabel("Team")
plt.tight_layout()
plt.show()

