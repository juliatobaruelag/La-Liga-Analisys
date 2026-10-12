import pandas as pd
import matplotlib.pyplot as plt

estadistiques = [
    "Punts",
    "Gols_per_partit",
    "Gols_encaixats",
    "Victories"
]


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
        "Equip": equip,
        "Partits": partits,
        "Punts": victories*3 + empats,
        "Victories": victories,
        "Empats" : empats,
        "Derrotes" : derrotes,
        "Gols" : gols,
        "Gols_per_partit" : gols_per_partit,
        "Gols_encaixats" : gols_encaixats,
        "Diferencia_gols" : gols - gols_encaixats,
        "Xuts" : xuts
    }

df = pd.read_csv("LaLiga_24-25.csv", low_memory=False)

equips = pd.unique(df["HomeTeam"])

data = []

for equip in equips:
    stat = estadistiques_equip(df,equip)
    data.append(stat)

classificacio = pd.DataFrame(data) #creem un dataframe de pandas
#reordenem les files i les indexem per punts
classificacio = classificacio.sort_values(by="Punts", ascending=False).reset_index(drop=True)

print("Top 5 Lliga 24/25\n")
print(classificacio)

classificacio_gols = classificacio.sort_values(by="Gols", ascending=False).reset_index(drop=True)
print("\nTop 5 Equips Golejadors Lliga 24/25\n")
print(classificacio_gols.head(5))

barca = classificacio[classificacio["Equip"] == "Barcelona"].iloc[0]
mitjana_lliga = classificacio.mean(numeric_only=True)

print("\n🔵🔴 Comparació Barça vs LaLiga")
for atr in estadistiques:
    atr_barca = barca[atr]
    atr_lliga = mitjana_lliga[atr]

    if(atr_barca > atr_lliga): 
        if(atr != "Gols_encaixats"): estat = " 🟢 MILLOR"
        else: estat = "🔴 PITJOR"
    elif (atr_barca == atr_lliga): estat = "IGUAL"
    else: 
        if(atr != "Gols_encaixats"): estat = "🔴 PITJOR"
        else: estat = " 🟢 MILLOR"
    print(f"{atr}: {atr_barca:.2f} vs {atr_lliga:.2f} -> {estat}")

    