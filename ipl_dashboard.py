import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import seaborn as sns
import streamlit as st
import kaggle

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="IPL Analysis Dashboard", page_icon="🏏", layout="wide")

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .block-container { padding-top: 1.5rem; }
    h1 { color: #f5a623; letter-spacing: 1px; }
    h2, h3 { color: #e0e0e0; }
    .stMetric { background: #1c2333; border-radius: 10px; padding: 12px; border-left: 4px solid #f5a623; }
    .stMetric label { color: #aaa !important; font-size: 0.8rem; }
    .stMetric [data-testid="stMetricValue"] { color: #f5a623 !important; font-size: 1.6rem; font-weight: 700; }
    .stTabs [data-baseweb="tab"] { font-size: 1rem; font-weight: 600; color: #aaa; }
    .stTabs [aria-selected="true"] { color: #f5a623 !important; border-bottom: 2px solid #f5a623; }
    .sidebar .sidebar-content { background-color: #1c2333; }
</style>
""", unsafe_allow_html=True)

st.title("🏏 IPL Analysis Dashboard (2008–2024)")

# ── SEABORN THEME ─────────────────────────────────────────────────────────────
sns.set_theme(style="darkgrid")
PALETTE_MAIN  = "YlOrRd"
PALETTE_BLUE  = "mako"
PALETTE_GREEN = "YlGnBu"
BG_COLOR      = "#0e1117"
PLOT_BG       = "#1c2333"
TEXT_COLOR     = "#e0e0e0"

def style_ax(ax, title=""):
    ax.set_facecolor(PLOT_BG)
    ax.figure.set_facecolor(PLOT_BG)
    ax.title.set_color(TEXT_COLOR)
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.tick_params(colors=TEXT_COLOR)
    for spine in ax.spines.values():
        spine.set_edgecolor("#333")
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", pad=12)

# ── DATA LOAD ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_and_clean_data():
    if not os.path.exists("matches.csv") or not os.path.exists("deliveries.csv"):
        os.environ["KAGGLE_USERNAME"] = st.secrets["KAGGLE_USERNAME"]
        os.environ["KAGGLE_KEY"]      = st.secrets["KAGGLE_KEY"]
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(
            "patrickb1912/ipl-complete-dataset-20082020",
            unzip=True
        )

    matches    = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")

    matches["city"]   = matches["city"].fillna("Unknown")
    matches["season"] = matches["season"].astype(str).str[:4].astype(int)

    team_map = {
        "Delhi Daredevils":        "Delhi Capitals",
        "Kings XI Punjab":         "Punjab Kings",
        "Rising Pune Supergiants": "Rising Pune Supergiant",
    }
    for df in [matches, deliveries]:
        for col in ["winner", "team1", "team2", "batting_team", "bowling_team"]:
            if col in df.columns:
                df[col] = df[col].replace(team_map)

    return matches, deliveries

with st.spinner("Loading IPL data..."):
    matches, deliveries = load_and_clean_data()

# ── SIDEBAR FILTERS ───────────────────────────────────────────────────────────
st.sidebar.header("🎯 Filters")

min_s, max_s = int(matches["season"].min()), int(matches["season"].max())
selected_seasons = st.sidebar.slider("Season Range", min_s, max_s, (min_s, max_s))

all_teams    = ["All Teams"] + sorted(
    pd.concat([matches["team1"], matches["team2"]]).dropna().unique().tolist()
)
selected_team = st.sidebar.selectbox("Team", all_teams)
top_n         = st.sidebar.slider("Top N players / venues", 5, 20, 10)

st.sidebar.markdown("---")
st.sidebar.caption("Data: Kaggle IPL Complete Dataset 2008–2024")

# ── APPLY FILTERS ─────────────────────────────────────────────────────────────
fm = matches[
    (matches["season"] >= selected_seasons[0]) &
    (matches["season"] <= selected_seasons[1])
]
if selected_team != "All Teams":
    fm = fm[(fm["team1"] == selected_team) | (fm["team2"] == selected_team)]
    fd = deliveries[
        deliveries["match_id"].isin(fm["id"]) &
        (deliveries["batting_team"] == selected_team)
    ]
else:
    fd = deliveries[deliveries["match_id"].isin(fm["id"])]

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
st.markdown("### 📊 Season Summary")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Matches Played",    len(fm))
k2.metric("Total Runs",        f"{int(fd['total_runs'].sum()):,}")
k3.metric("Total Wickets",     int(fd["is_wicket"].sum()))
k4.metric("Total Sixes",       int((fd["batsman_runs"] == 6).sum()))

st.markdown("---")

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🏆 Team Analysis",
    "🏏 Batting",
    "🎯 Bowling",
    "📈 Trends & Venues",
])

# ════════════════════════════════════════════════════════════
# TAB 1 — TEAM ANALYSIS
# ════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns(2)

    # Chart 1 — Most wins
    with col1:
        st.subheader(f"Most Wins ({selected_seasons[0]}–{selected_seasons[1]})")
        wins = fm["winner"].value_counts().reset_index().head(top_n)
        wins.columns = ["team", "wins"]
        if not wins.empty:
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.barplot(data=wins, x="wins", y="team", palette=PALETTE_MAIN, ax=ax)
            style_ax(ax, "Most Wins by Team")
            ax.set_xlabel("Wins", color=TEXT_COLOR)
            ax.set_ylabel("Team", color=TEXT_COLOR)
            st.pyplot(fig); plt.close(fig)
        else:
            st.warning("No data for this selection.")

    # Chart 2 — Toss decision
    with col2:
        st.subheader("Toss Decision")
        toss = fm["toss_decision"].value_counts()
        if not toss.empty:
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(
                toss, labels=toss.index, autopct="%1.1f%%",
                startangle=90, colors=["#f5a623", "#2b5c8f"],
                textprops={"color": TEXT_COLOR}
            )
            ax.set_facecolor(PLOT_BG)
            fig.set_facecolor(PLOT_BG)
            ax.set_title("Bat vs Field", color=TEXT_COLOR, fontsize=13, fontweight="bold")
            st.pyplot(fig); plt.close(fig)
        else:
            st.warning("No toss data.")

    col3, col4 = st.columns(2)

    # Chart 3 — Highest team innings
    with col3:
        st.subheader("Highest Team Innings Totals")
        inn = deliveries[deliveries["match_id"].isin(fm["id"])]
        team_totals = (
            inn.groupby(["match_id", "batting_team"])["total_runs"]
            .sum().reset_index()
            .sort_values("total_runs", ascending=False)
            .head(top_n)
        )
        if not team_totals.empty:
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.barplot(data=team_totals, x="total_runs", y="batting_team", palette="magma", ax=ax)
            style_ax(ax, "Highest Team Totals in a Single Innings")
            ax.set_xlabel("Total Runs", color=TEXT_COLOR)
            ax.set_ylabel("Team", color=TEXT_COLOR)
            st.pyplot(fig); plt.close(fig)
        else:
            st.warning("No innings data.")

    # Chart 4 — Wins heatmap
    with col4:
        st.subheader("Team Wins Per Season (Heatmap)")
        pivot = fm.groupby(["winner", "season"]).size().unstack(fill_value=0)
        if not pivot.empty:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.heatmap(
                pivot, annot=True, fmt="d", cmap=PALETTE_GREEN,
                ax=ax, cbar=False,
                annot_kws={"size": 8},
                linewidths=0.4, linecolor="#0e1117"
            )
            style_ax(ax, "Team Wins Per Season")
            ax.set_xlabel("Season", color=TEXT_COLOR)
            ax.set_ylabel("Team", color=TEXT_COLOR)
            plt.tight_layout()
            st.pyplot(fig); plt.close(fig)
        else:
            st.warning("Not enough data for heatmap.")

# ════════════════════════════════════════════════════════════
# TAB 2 — BATTING
# ════════════════════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns(2)

    # Chart 5 — Top run scorers
    with col1:
        st.subheader(f"Top {top_n} Run Scorers")
        top_scorers = (
            fd.groupby("batter")["batsman_runs"]
            .sum().reset_index()
            .sort_values("batsman_runs", ascending=False)
            .head(top_n)
        )
        top_scorers.columns = ["batter", "total_runs"]
        if not top_scorers.empty:
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.barplot(data=top_scorers, x="total_runs", y="batter", palette=PALETTE_MAIN, ax=ax)
            style_ax(ax, f"Top {top_n} Run Scorers")
            ax.set_xlabel("Total Runs", color=TEXT_COLOR)
            ax.set_ylabel("Batter", color=TEXT_COLOR)
            st.pyplot(fig); plt.close(fig)
        else:
            st.warning("No batting data.")

    # Chart 6 — Top boundary hitters
    with col2:
        st.subheader(f"Top {top_n} Boundary Hitters")
        bounds = (
            fd[fd["batsman_runs"].isin([4, 6])]
            .groupby("batter")["batsman_runs"]
            .count().reset_index()
            .sort_values("batsman_runs", ascending=False)
            .head(top_n)
        )
        bounds.columns = ["batter", "boundaries"]
        if not bounds.empty:
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.barplot(data=bounds, x="boundaries", y="batter", palette="flare", ax=ax)
            style_ax(ax, f"Top {top_n} Boundary Hitters")
            ax.set_xlabel("Boundaries (4s + 6s)", color=TEXT_COLOR)
            ax.set_ylabel("Batter", color=TEXT_COLOR)
            st.pyplot(fig); plt.close(fig)
        else:
            st.warning("No boundary data.")

    col3, col4 = st.columns(2)

    # Chart 7 — Runs vs boundaries scatter
    with col3:
        st.subheader("Runs vs Boundaries (Scatter)")
        runs_all = fd.groupby("batter")["batsman_runs"].sum().reset_index()
        runs_all.columns = ["batter", "total_runs"]
        bounds_all = (
            fd[fd["batsman_runs"].isin([4, 6])]
            .groupby("batter")["batsman_runs"].count().reset_index()
        )
        bounds_all.columns = ["batter", "boundaries"]
        scatter_df = runs_all.merge(bounds_all, on="batter")
        if not scatter_df.empty:
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.scatterplot(
                data=scatter_df, x="total_runs", y="boundaries",
                alpha=0.6, color="#f5a623", ax=ax
            )
            style_ax(ax, "Runs vs Boundaries per Batter")
            ax.set_xlabel("Total Runs", color=TEXT_COLOR)
            ax.set_ylabel("Boundaries", color=TEXT_COLOR)
            st.pyplot(fig); plt.close(fig)
        else:
            st.warning("No scatter data.")

    # Chart 8 — Player of the Match
    with col4:
        st.subheader(f"Top {top_n} Player of the Match Awards")
        potm = fm["player_of_match"].value_counts().reset_index().head(top_n)
        potm.columns = ["player", "awards"]
        if not potm.empty:
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.barplot(data=potm, x="awards", y="player", palette="crest", ax=ax)
            style_ax(ax, f"Top {top_n} Player of the Match Awards")
            ax.set_xlabel("Awards", color=TEXT_COLOR)
            ax.set_ylabel("Player", color=TEXT_COLOR)
            st.pyplot(fig); plt.close(fig)
        else:
            st.warning("No POTM data.")

# ════════════════════════════════════════════════════════════
# TAB 3 — BOWLING
# ════════════════════════════════════════════════════════════
with tab3:
    col1, col2 = st.columns(2)

    # Chart 9 — Top wicket takers
    with col1:
        st.subheader(f"Top {top_n} Wicket Takers")
        bowl_fd = deliveries[deliveries["match_id"].isin(fm["id"])]
        top_wickets = (
            bowl_fd[
                (bowl_fd["is_wicket"] == 1) &
                (~bowl_fd["dismissal_kind"].isin(["run out", "retired hurt", "obstructing the field"]))
            ]
            .groupby("bowler")["is_wicket"]
            .sum().reset_index()
            .sort_values("is_wicket", ascending=False)
            .head(top_n)
        )
        top_wickets.columns = ["bowler", "wickets"]
        if not top_wickets.empty:
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.barplot(data=top_wickets, x="wickets", y="bowler", palette=PALETTE_BLUE, ax=ax)
            style_ax(ax, f"Top {top_n} Wicket Takers")
            ax.set_xlabel("Wickets", color=TEXT_COLOR)
            ax.set_ylabel("Bowler", color=TEXT_COLOR)
            st.pyplot(fig); plt.close(fig)
        else:
            st.warning("No bowling data.")

    # Chart 10 — Dismissal types
    with col2:
        st.subheader("Dismissal Types Breakdown")
        dismissals = bowl_fd[bowl_fd["is_wicket"] == 1]["dismissal_kind"].value_counts()
        if not dismissals.empty:
            fig, ax = plt.subplots(figsize=(6, 5))
            colors = sns.color_palette("mako", len(dismissals))
            ax.pie(
                dismissals, labels=dismissals.index, autopct="%1.1f%%",
                startangle=90, colors=colors,
                textprops={"color": TEXT_COLOR, "fontsize": 8}
            )
            ax.set_facecolor(PLOT_BG)
            fig.set_facecolor(PLOT_BG)
            ax.set_title("How Batters Get Out", color=TEXT_COLOR, fontsize=13, fontweight="bold")
            st.pyplot(fig); plt.close(fig)
        else:
            st.warning("No dismissal data.")

# ════════════════════════════════════════════════════════════
# TAB 4 — TRENDS & VENUES
# ════════════════════════════════════════════════════════════
with tab4:
    col1, col2 = st.columns(2)

    # Chart 11 — Total runs per season
    with col1:
        st.subheader("Total Runs Per Season")
        season_runs = (
            deliveries[deliveries["match_id"].isin(fm["id"])]
            .merge(fm[["id", "season"]], left_on="match_id", right_on="id")
            .groupby("season")["total_runs"].sum().reset_index()
        )
        if not season_runs.empty:
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.barplot(data=season_runs, x="season", y="total_runs", palette=PALETTE_MAIN, ax=ax)
            style_ax(ax, "Total Runs Scored Per Season")
            ax.set_xlabel("Season", color=TEXT_COLOR)
            ax.set_ylabel("Total Runs", color=TEXT_COLOR)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig); plt.close(fig)
        else:
            st.warning("No season data.")

    # Chart 12 (bonus!) — Top venues
    with col2:
        st.subheader(f"Top {top_n} Venues by Matches Hosted")
        venue = fm["venue"].value_counts().reset_index().head(top_n)
        venue.columns = ["venue", "matches"]
        if not venue.empty:
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.barplot(data=venue, x="matches", y="venue", palette="crest", ax=ax)
            style_ax(ax, f"Top {top_n} Venues")
            ax.set_xlabel("Matches Hosted", color=TEXT_COLOR)
            ax.set_ylabel("Venue", color=TEXT_COLOR)
            st.pyplot(fig); plt.close(fig)
        else:
            st.warning("No venue data.")

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Built with ❤️ using Python · Pandas · Seaborn · Streamlit | Data: Kaggle IPL Dataset 2008–2024")
