# 📊 LaLiga Analysis  

## 🧠 Project Description
This project is a practical introduction to **data science with Python**, applied to football analysis, specifically **LaLiga**.

The main goal is to **learn Python, basic data analysis, and machine learning** (`pandas`, `matplotlib`, and `scikit-learn`) through a project that **evolves in phases**, starting with descriptive analysis and progressing to the creation of match prediction models.

The project is developed incrementally, adding new functionalities as new concepts and libraries are learned.

---

## 🛠️ Technologies Used
- **Python 3**
- **pandas** → data manipulation, filtering, and aggregation
- **matplotlib** → data visualization and charting
- **scikit-learn** → machine learning models (`RandomForestClassifier`, `LabelEncoder`)
- **CSV files** → match data from LaLiga

---

## 📂 Data
The dataset corresponds to the **2024-2025 LaLiga season** (`LaLiga_24-25.csv`) and includes, among others:

- Home and away teams (`HomeTeam`, `AwayTeam`)
- Match results (`FTHG`, `FTAG`, `FTR`)
- Goals scored and conceded
- Shots, fouls, and corners (`HS`, `AS`, `HF`, `AF`, `HC`, `AC`)
- Yellow and red cards (`HY`, `AY`, `HR`, `AR`)

---

## 📌 Project Structure

### 🔹 Phase 1 – Basic Analysis (`fase1.py` & `llegir_csv.py`)
- Explore the CSV file and handle data structures.
- Filter FC Barcelona matches.
- Calculate:
  - Wins, draws, and losses.
  - Goals scored and conceded.
- Initial plots:
  - Result distribution (Wins/Draws/Losses).
  - Goals histogram.

🎯 Goal: learn how to read CSV files and perform basic statistics with pandas.

---

### 🔹 Phase 2 – Home vs Away (`fase2.py`)
- Separate a selected team's matches into:
  - Home
  - Away
- Performance comparison:
  - Win percentage.
  - Goals per match and goals conceded.
  - Attack efficiency (Goals / Shots).
  - Discipline (Fouls, yellow/red cards).
- Comparative plots for home and away scenarios.

🎯 Goal: gain a better understanding of the data, calculate derived metrics, and compare specific scenarios.

---

### 🔹 Phase 3 – Team Comparison & League Standings (`fase3.1.py` & `fase3.2.py`)
- Create a **reusable function** (`estadistiques_equip`) to calculate any team's statistics.
- Direct head-to-head comparison of two user-selected teams (Points, Goals, Shots, etc.).
- Generate the League Standings (Top 5 teams by points).
- Generate Top Scoring Teams (Top 5 by goals).
- Compare a specific team (e.g., Barcelona) against the overall LaLiga average.

🎯 Goal: structure the code professionally, avoid duplication using functions, and aggregate league-wide data.

---

### 🔹 Phase 4 – Heuristic Match Prediction (`fase4.py`)
- Algorithm to calculate team "Strength" (`calcular_forca`) based on weighted stats (Goals per match, points, wins, conceded goals).
- Algorithm to calculate the Head-to-Head score (`h2h_score`) based on direct confrontation history.
- Custom prediction function combining team strength (75% weight) and H2H record (25% weight) to forecast the winner or a likely draw.

🎯 Goal: Use calculated metrics to build a logical, rule-based predictive model.

---

### 🔹 Phase 5 – Machine Learning Prediction (`fase5.py`)
- Build a structured dataset containing features: `forca_home`, `forca_away`, and `h2h`.
- Encode categorical results (`LabelEncoder`).
- Split data into training and testing sets (`train_test_split`).
- Train an AI model using **Random Forest** (`RandomForestClassifier`) with 100 decision trees.
- Evaluate the model's accuracy and create a functional ML prediction pipeline.

🎯 Goal: Transition from heuristic rules to actual Machine Learning models that learn patterns from historical data.

---

## 👨‍💻 Author
Developed as a **learning project for Python, data science, and machine learning**, with a practical and progressive approach.
