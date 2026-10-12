import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("LaLiga_24-25.csv", low_memory=False)

team = input("Select team: ")

# HOME
print("🏟️  HOME")

home_team = df[df["HomeTeam"] == team]

home_wins = home_team[home_team["FTR"] == "H"]
home_win_percentage = len(home_wins) / len(home_team)

print(f"% Wins: {home_win_percentage:.2%}")

home_goals = home_team["FTHG"].sum()
print(f"Goals scored: {home_goals}")

home_goals_per_match = home_goals / len(home_team)
print(f"Goals per match: {home_goals_per_match:.2}")

home_goals_conceded = home_team["FTAG"].sum()
print(f"Goals conceded: {home_goals_conceded}")

home_goals_conceded_per_match = home_goals_conceded / len(home_team)
print(f"Goals conceded per match: {home_goals_conceded_per_match:.2}")

print("Goal difference:", home_goals - home_goals_conceded)

home_shots = home_team["HS"].sum()
attack_efficiency = home_goals / home_shots
print(f"Attack efficiency: {attack_efficiency:.2}")

fouls_received = home_team["AF"].sum()
fouls_committed = home_team["HF"].sum()
print("Fouls:", fouls_committed, "-", fouls_received)

home_corners = home_team["HC"].sum()
away_corners = home_team["AC"].sum()
print("Corners:", home_corners, "-", away_corners)

home_yellow_cards = home_team["HY"].sum()
away_yellow_cards = home_team["AY"].sum()
print("Yellow cards:", home_yellow_cards, "-", away_yellow_cards)

home_red_cards = home_team["HR"].sum()
away_red_cards = home_team["AR"].sum()
print("Red cards:", home_red_cards, "-", away_red_cards)


# AWAY
print("\n✈️  AWAY")

away_team = df[df["AwayTeam"] == team]

away_wins = away_team[away_team["FTR"] == "A"]
away_win_percentage = len(away_wins) / len(away_team)

print(f"% Wins: {away_win_percentage:.2%}")

away_goals = away_team["FTAG"].sum()
print(f"Goals scored: {away_goals}")

away_goals_per_match = away_goals / len(away_team)
print(f"Goals per match: {away_goals_per_match:.2}")

away_goals_conceded = away_team["FTHG"].sum()
print(f"Goals conceded: {away_goals_conceded}")

away_goals_conceded_per_match = away_goals_conceded / len(away_team)
print(f"Goals conceded per match: {away_goals_conceded_per_match:.2}")

print("Goal difference:", away_goals - away_goals_conceded)

away_shots = away_team["AS"].sum()
attack_efficiency = away_goals / away_shots
print(f"Attack efficiency: {attack_efficiency:.2}")

fouls_committed = away_team["AF"].sum()
fouls_received = away_team["HF"].sum()
print("Fouls:", fouls_received, "-", fouls_committed)

home_corners = away_team["HC"].sum()
away_corners = away_team["AC"].sum()
print("Corners:", home_corners, "-", away_corners)

home_yellow_cards = away_team["HY"].sum()
away_yellow_cards = away_team["AY"].sum()
print("Yellow cards:", home_yellow_cards, "-", away_yellow_cards)

home_red_cards = away_team["HR"].sum()
away_red_cards = away_team["AR"].sum()
print("Red cards:", home_red_cards, "-", away_red_cards)


# Charts
categories = ["Home", "Away"]
goals_scored = [home_goals, away_goals]
goals_conceded = [home_goals_conceded, away_goals_conceded]

x = range(len(categories))
bar_width = 0.35

plt.bar([i - bar_width / 2 for i in x], goals_scored, width=bar_width, label="Goals scored", color="blue")
plt.bar([i + bar_width / 2 for i in x], goals_conceded, width=bar_width, label="Goals conceded", color="red")

plt.xticks(x, categories)
plt.ylabel("Goals")
plt.title("Goals: Home vs Away")
plt.legend()
plt.show()
