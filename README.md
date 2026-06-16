# 🏏 IPL Analysis Dashboard (2008–2024)

An interactive data analysis dashboard built with Python and Streamlit, analyzing IPL cricket data across 17 seasons.

🚀 **[Live Demo](https://ipl-dashboard-kxyp7dega797mbnwsv442q.streamlit.app/)**

---

## ✨ Features

- 🎯 **Interactive Filters** — filter by season range, team, and top N players/venues
- 📊 **KPI Cards** — instant summary of matches, runs, wickets and sixes
- 🗂️ **4 Organised Tabs** — Team Analysis, Batting, Bowling, Trends & Venues
- 🌙 **Dark Theme** — custom styled UI with orange accent colors

---

## 📈 What's Inside

### 🏆 Team Analysis
- Most wins by team
- Toss decision breakdown (Bat vs Field)
- Highest team total in a single innings
- Team wins per season heatmap

### 🏏 Batting
- Top run scorers
- Top boundary hitters (4s + 6s)
- Runs vs boundaries scatter plot
- Most Player of the Match awards

### 🎯 Bowling
- Top wicket takers (excludes run outs)
- Dismissal types breakdown

### 📈 Trends & Venues
- Total runs scored per season
- Top venues by matches hosted

---

## 🛠️ Built With

- Python
- Pandas
- Matplotlib
- Seaborn
- Streamlit

---

## 📂 Dataset

IPL Complete Dataset from Kaggle (2008–2024) — auto downloaded via Kaggle API on deployment.

---

## 🚀 Run Locally

```bash
git clone https://github.com/devs-here/ipl-dashboard.git
cd ipl-dashboard
pip install -r requirements.txt
streamlit run ipl_dashboard.py
```

> Add your Kaggle credentials to `.streamlit/secrets.toml`:
> ```
> KAGGLE_USERNAME = "your_username"
> KAGGLE_KEY = "your_api_key"
> ```
