import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

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

def predir_partit(df, equip1, equip2):
    f1 = calcular_forca(df,equip1)
    f2 = calcular_forca(df,equip2)

    h2h_1 = h2h_score(df,equip1,equip2)
    h2h_2 = 1 - h2h_1

    pred1 = 0.75 * f1 + 0.25 * h2h_1
    pred2 = 0.75 * f2 + 0.25 * h2h_2

    if pred1 > pred2 + 0.15:
        resultat = f"Guanya {equip1}"
    elif pred2 > pred1 + 0.15:
        resultat = f"Guanya {equip2}"
    else:
        resultat = "Empat probable"

    return {
        "equip1": equip1,
        "equip2": equip2,
        "forca1": f1,
        "forca2": f2,
        "h2h1": h2h_1,
        "h2h2": h2h_2,
        "pred1": pred1,
        "pred2": pred2,
        "resultat": resultat
    }

def constuir_dataset(df):
    files = []

    for _, row in df.iterrows():
        home = row["HomeTeam"]
        away = row["AwayTeam"]

        files.append({
            "forca_home": calcular_forca(df,home),
            "forca_away": calcular_forca(df,away),
            "h2h": h2h_score(df,home,away),
            "resultat": row["FTR"]
        })

    return pd.DataFrame(files)


df = pd.read_csv("LaLiga_24-25.csv", low_memory=False)

dataset = constuir_dataset(df)

X = dataset[["forca_home","forca_away","h2h"]]
y = dataset["resultat"]

le = LabelEncoder()
y = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train,y_train)

accuracy = model.score(X_test,y_test)

def predir_partit_ml(df, model, equip1, equip2):
    X_nou = pd.DataFrame([{
        "forca_home": calcular_forca(df, equip1),
        "forca_away": calcular_forca(df, equip2),
        "h2h": h2h_score(df, equip1, equip2)
    }])

    pred = model.predict(X_nou)[0]
    return le.inverse_transform([pred])[0]

def validar_equip(df, equip):
    equips = set(df["HomeTeam"]).union(set(df["AwayTeam"]))
    return equip in equips


equip1 = input("Equip local: ")
equip2 = input("Equip visitant: ")

if not validar_equip(df, equip1):
    print(f"❌ Error: l'equip '{equip1}' no existeix a la base de dades.")
    exit()

if not validar_equip(df, equip2):
    print(f"❌ Error: l'equip '{equip2}' no existeix a la base de dades.")
    exit()


resultat = predir_partit_ml(df, model, equip1, equip2)

if resultat == 1:
    print(f"Predicció ML: {equip1}")
elif resultat == -1: 
    print(f"Predicció ML: {equip2}")
else:
    print(f"Predicció ML: Draw")

print(f"Precisió del model: {accuracy:.2%}")