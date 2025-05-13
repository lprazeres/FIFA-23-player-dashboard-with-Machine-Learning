# ⚽ FIFA 23 Player Dashboard with Machine Learning

This project combines Exploratory Data Analysis (EDA), Machine Learning, Clustering, and Interactive Dashboards to extract insights and generate value from the FIFA 23 player database.

---

## 📊 Project Overview

### 🔍 Exploratory Data Analysis (EDA)
- Analyzed how different nationalities influence player market value.
- Identified which countries tend to inflate player prices the most.
- Suggested strategic countries to scout for more cost-effective talent.

### 🤖 Machine Learning
- Identified the **top 5 features** that most influence the **Overall Rating** for each player position using feature importance techniques.
- Trained separate ML models for each position to predict Overall Rating based on these 5 key features.
- Saved all trained models using `pickle` in the `/models/` directory.

### 📈 Clustering Analysis
- Applied **KMeans Clustering** to group players based on salary and market value.
- Helped identify which players offer **higher returns on investment**.
- Visualized clusters to highlight potential undervalued or overpaid players.

### 🌐 Dashboard (Streamlit)
- Developed an interactive **Streamlit dashboard** to present insights.
- Enables filtering by nationality, position, and more.
- Includes ML predictions and clustering results in a user-friendly interface.

---

## 🧰 Tech Stack & Libraries

- **Programming Language**: Python  
- **Database**: SQLite (`sqlite3`)
- **Data Handling**: `pandas`
- **Visualization**: `matplotlib`, `seaborn`
- **Statistics**: `scipy`
- **Machine Learning**: `scikit-learn`, `numpy`
- **Model Deployment**: `pickle`
- **Web App**: `streamlit`

---

## 🗃️ Data

- The dataset used is from FIFA 23, structured in an SQLite database.
- SQL queries and joins were performed to extract and transform the data for analysis and modeling.
