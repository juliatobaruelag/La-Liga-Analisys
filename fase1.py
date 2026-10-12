import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("LaLiga_24-25.csv", low_memory=False)  # df = DataFrame

# Filter Barcelona matches
barca = df[(df["HomeTeam"] == "Barcelona") | (df["AwayTeam"] == "Barcelona")]

# Add Barcelona goals column
def barcelona_goals(row):
    if row["HomeTeam"] == "Barcelona":
        return row["FTHG"]
    else:
        return row["FTAG"]

# Modifying columns of a filtered DataFrame may not affect the original
barca = barca.copy()
barca["BarcelonaGoals"] = barca.apply(barcelona_goals, axis=1)

wins = barca[
    ((barca["HomeTeam"] == "Barcelona") & (barca["FTR"] == "H")) |
    ((barca["AwayTeam"] == "Barcelona") & (barca["FTR"] == "A"))
]

draws = barca[barca["FTR"] == "D"]

losses = barca[
    ((barca["HomeTeam"] == "Barcelona") & (barca["FTR"] == "A")) |
    ((barca["AwayTeam"] == "Barcelona") & (barca["FTR"] == "H"))
]

print("Wins =", len(wins))
print("Draws =", len(draws))
print("Losses =", len(losses))

# Results distribution chart
categories = ["Wins", "Draws", "Losses"]
values = [len(wins), len(draws), len(losses)]

plt.bar(categories, values, color=["blue", "red", "yellow"])
plt.title("FC Barcelona Results")
plt.xlabel("Result")
plt.ylabel("Number of matches")
plt.show()

# Goals histogram
goals = barca["BarcelonaGoals"]

plt.hist(goals, bins=range(0, int(goals.max()) + 2), edgecolor="blue")
plt.title("Distribution of Barcelona Goals")
plt.xlabel("Goals per match")
plt.ylabel("Number of matches")
plt.show()
