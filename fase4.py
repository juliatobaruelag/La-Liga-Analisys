import pandas as pd
import matplotlib.pyplot as plt

estadistiques = [
    "Punts",
    "Gols_per_partit",
    "Gols_encaixats",
    "Victories"
]

def calcular_forca(df,equip):
    stats = estadistiques_equip(df,equip)

    partits = stats["Partits"]
    punts_partit = stats["Punts"]/partits
    gols_partit = stats["Gols_per_partit"]/partits
    gols_encaixats_partit = stats["Gols_encaixats"]/partits
    victories_partit = stats["Victories"]/partits

    return 0.40 * gols_partit + 0.3 * punts_partit + 0.2 * victories_partit - 0.3 * gols_encaixats_partit 

def h2h_score(df, equip1, equip2):
    partits = df[
        ((df["HomeTeam"] == equip1) & (df["AwayTeam"] == equip2)) |
        ((df["HomeTeam"] == equip2) & (df["AwayTeam"] == equip1))
    ]

    if len(partits) == 0:
        return 0.5  

    punts1 = 0
    gols1 = 0
    gols2 = 0

    for _, row in partits.iterrows():
        if row["HomeTeam"] == equip1:
            gols1 += row["FTHG"]
            gols2 += row["FTAG"]
            if row["FTR"] == "H":
                punts1 += 3
            elif row["FTR"] == "D":
                punts1 += 1
        else:
            gols1 += row["FTAG"]
            gols2 += row["FTHG"]
            if row["FTR"] == "A":
                punts1 += 3
            elif row["FTR"] == "D":
                punts1 += 1

    max_punts = len(partits) * 3
    punts_score = punts1 / max_punts          # 0–1

    dif_gols = gols1 - gols2
    dif_score = 0.5 + (dif_gols / (abs(dif_gols) + 1)) * 0.5  # 0–1

    encaixats_score = 1 / (1 + gols2)          

    # Score final ponderat
    h2h = (0.5 * punts_score + 0.3 * dif_score + 0.2 * encaixats_score)

    return h2h


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

equip1 = input("Equip1: ")
equip2 = input("Equip2: ")

f1 = calcular_forca(df,equip1)
f2 = calcular_forca(df,equip2)

h2h_1 = h2h_score(df,equip1,equip2)
h2h_2 = 1 - h2h_1

pred1 = 0.75 * f1 + 0.25 * h2h_1
pred2 = 0.75 * f2 + 0.25 * h2h_2

if pred1 > pred2 + 0.15:
    print(f"Predicció: Guanya {equip1}")
elif pred2 > pred1 + 0.15:
    print(f"Predicció: Guanya {equip2}")
else:
    print("Predicció: Empat probable")
