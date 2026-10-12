import pandas as pd
import matplotlib.pyplot as plt

def estadistiques_equip(df, equip):
    local = df[df["HomeTeam"] == equip]
    visitant = df[df["AwayTeam"] == equip]

    partits = len(local) + len(visitant)

    victories = len(local[local["FTR"] == "H"]) + len(visitant[visitant["FTR"] == "A"])
    derrotes = len(local[local["FTR"] == "A"]) + len(visitant[visitant["FTR"] == "H"])
    empats = partits - victories - derrotes

    gols = local["FTHG"].sum() + visitant["FTAG"].sum()
    gols_per_partit = gols/partits
    gols_encaixats = local["FTAG"].sum() + visitant["FTHG"].sum()

    xuts = local["HS"].sum() + visitant["AS"].sum()

    return {
        "partits": partits,
        "punts": victories*3 + empats,
        "victories": victories,
        "empats" : empats,
        "derrotes" : derrotes,
        "gols" : gols,
        "gols_per_partit" : gols_per_partit,
        "gols_encaixats" : gols_encaixats,
        "diferencia_gols" : gols - gols_encaixats,
        "xuts" : xuts
    }

df = pd.read_csv("LaLiga_24-25.csv", low_memory=False)

team1 = input("Selecciona el primer equip: ")
team2 = input("Selecciona el segon equip: ")

est_t1 = estadistiques_equip(df,team1)
est_t2 = estadistiques_equip(df,team2)


print("📊  Comparació")
print(team1 + "VS" + team2)
for estad in est_t1:
    v1 = est_t1[estad]
    v2 = est_t2[estad]
    if isinstance(v1,float):
        print(f"{estad}: {v1:.2f} | {v2:.2f}")
    else:
        print(f"{estad}: {v1} | {v2}")


equips = [team1, team2]
gols = [est_t1["gols"], est_t2["gols"]]
dif = [est_t1["diferencia_gols"], est_t2["diferencia_gols"]]
x = range(len(equips))

plt.bar([i - 0.2 for i in x], gols, width = 0.4, label = "Gols marcats")
plt.bar([i + 0.2 for i in x], dif, width = 0.4, label = "Diferència gols")
plt.title("Comparació ofensiva")
plt.legend()
plt.show()