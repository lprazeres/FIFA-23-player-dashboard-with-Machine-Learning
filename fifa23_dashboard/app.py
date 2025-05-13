import streamlit as st
import sqlite3
import pandas as pd
import pickle
import os
import numpy as np
import plotly.express as px

# App title
st.title("FIFA 23 Player Dashboard")

# Connect to the database
conn = sqlite3.connect('C:/Users/lpraz/OneDrive/Área de Trabalho/Masters Degree/12 - Portfolio Machine Learning/05 - FIFA 23/fifa23_dashboard/data/fifa23.db')

# Top 5 features per position
top5_features_by_position = {
    "ST_CF": ["Finishing", "Positioning", "BallControl", "Shot Power", "Dribbling"],
    "CAM": ["BallControl", "Dribbling", "Short Passing", "Physicality Total", "Vision"],
    "CM": ["Short Passing", "BallControl", "Vision", "LongPassing", "Defending Total"],
    "RM_RW": ["Crossing", "Dribbling", "Finishing", "Physicality Total", "Shooting Total"],
    "GK": ["Reactions", "Dribbling Total", "Goalkeeper Reflexes", "Goalkeeper Positioning", "Physicality Total"],
    "CB": ["Standing Tackle", "Marking", "Interceptions", "Strength", "Heading Accuracy"],
    "LM_LW": ["Dribbling", "BallControl", "Crossing", "Positioning", "Short Passing"],
    "CDM": ["Interceptions", "BallControl", "Marking", "Standing Tackle", "Short Passing"],
    "LB_LWB": ["Crossing", "Sliding Tackle", "Interceptions", "Standing Tackle", "Short Passing"],
    "RB_RWB": ["Crossing", "Sliding Tackle", "Interceptions", "Pace Total", "Standing Tackle"],
}

# Query to get unique positions
query_positions = """
SELECT DISTINCT GroupedPosition
FROM players_fifa23
WHERE GroupedPosition IS NOT NULL
ORDER BY GroupedPosition;
"""
positions = pd.read_sql_query(query_positions, conn)
position_list = positions["GroupedPosition"].tolist()

# Sidebar with position selection
selected_positions = st.sidebar.multiselect(
    "Select positions:", 
    options=position_list,
    default=position_list
)


# Logic for one position selected
if len(selected_positions) == 1:
    selected_position = selected_positions[0]
    st.sidebar.markdown("### 🔍 Predict Overall")
    st.sidebar.write(f"Model for position: **{selected_position}**")

    features = top5_features_by_position.get(selected_position, [])
    input_values = {}
    for feat in features:
        input_values[feat] = st.sidebar.number_input(f"{feat}", min_value=0, max_value=100, value=75)

    model_path = f"C:/Users/lpraz/OneDrive/Área de Trabalho/Masters Degree/12 - Portfolio Machine Learning/05 - FIFA 23/fifa23_dashboard/models/model_{selected_position}.pkl"

    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            model = pickle.load(f)

        input_array = np.array([input_values[feat] for feat in features]).reshape(1, -1)
        predicted_overall = model.predict(input_array)[0]
        st.sidebar.success(f"🎯 Predicted Overall: {predicted_overall:.0f}")

        min_overall = predicted_overall - 3
        max_overall = predicted_overall + 3

        query_filtered = f"""
        SELECT p.*, c.value_cluster_label, c.wage_cluster_label
        FROM players_fifa23 p
        LEFT JOIN players_fifa23_with_clusters c ON p.player_id = c.player_id
        WHERE p.GroupedPosition = '{selected_position}'
        AND p.Overall BETWEEN {min_overall} AND {max_overall};
        """
        df_filtered = pd.read_sql_query(query_filtered, conn)

        st.write(f"🎯 Players with Overall between {min_overall:.0f} and {max_overall:.0f} (position: {selected_position}):")
        st.dataframe(df_filtered)


    else:
        st.sidebar.error(f"❌ Model for {selected_position} not found.")

# Logic for multiple positions selected
elif len(selected_positions) > 1:
    placeholder = "','".join(selected_positions)
    query_filtered = f"""
    SELECT p.*, c.value_cluster_label, c.wage_cluster_label
    FROM players_fifa23 p
    LEFT JOIN players_fifa23_with_clusters c ON p.player_id = c.player_id
    WHERE p.GroupedPosition IN ('{placeholder}');
    """
    df_filtered = pd.read_sql_query(query_filtered, conn)

    st.write("📌 Players filtered by selected positions:")
    st.dataframe(df_filtered)


else:
    st.warning("Please select at least one position to proceed.")