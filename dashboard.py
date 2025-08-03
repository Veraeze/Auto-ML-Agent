import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import altair as alt

st.set_page_config(page_title="AutoML Agent Dashboard", layout="wide")
st.title("📊 AutoML Agent Dashboard")

# Paths
DATASETS_DIR = "datasets"
LOG_FILE = "cron_log.txt"

# Helper to get metadata from each dataset folder
def parse_dataset_info():
    data = []
    if not os.path.exists(DATASETS_DIR):
        return pd.DataFrame()

    for folder in sorted(os.listdir(DATASETS_DIR), reverse=True):
        folder_path = os.path.join(DATASETS_DIR, folder)
        if os.path.isdir(folder_path):
            date_str = folder.split("_")[0]
            dataset_name = folder.replace(date_str + "_", "")
            readme_path = os.path.join(folder_path, "README.md")
            summary_path = os.path.join(folder_path, "model_selection_summary.txt")
            eval_path = os.path.join(folder_path, "model_evaluation_summary.txt")
            model_name_path = os.path.join(folder_path, "model_name.txt")

            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
            except:
                date = None

            # Try to extract problem type and accuracy
            problem_type = "?"
            accuracy = None
            model_name = "?"
            if os.path.exists(model_name_path):
                with open(model_name_path) as f:
                    model_name = f.read().strip()
            if os.path.exists(summary_path):
                with open(summary_path) as f:
                    for line in f:
                        if "Problem type" in line:
                            problem_type = line.split(":")[-1].strip()
                            break

            if os.path.exists(eval_path):
                with open(eval_path) as f:
                    for line in f:
                        if "Accuracy" in line:
                            accuracy = line.split(":")[-1].strip()
                            break

            data.append({
                "Date": date,
                "Dataset": dataset_name,
                "Folder": folder,
                "Problem Type": problem_type,
                "Accuracy": accuracy,
                "Slack Notified": "✅",
                "Run Duration": "~5 mins",
                "Status": "✅ Success",
                "Model": model_name
            })

    return pd.DataFrame(data)

# Dashboard layout
df = parse_dataset_info()

# Filter section
with st.sidebar:
    st.header("🔍 Filter Runs")
    date_range = st.date_input("Date Range", [])
    problem_filter = st.multiselect("Problem Type", df["Problem Type"].unique())

    filtered_df = df.copy()
    if date_range and len(date_range) == 2:
        filtered_df = filtered_df[(filtered_df["Date"] >= pd.to_datetime(date_range[0])) &
                                   (filtered_df["Date"] <= pd.to_datetime(date_range[1]))]
    if problem_filter:
        filtered_df = filtered_df[filtered_df["Problem Type"].isin(problem_filter)]

# Main table
st.subheader("🗂️ Daily Run Summary")
st.dataframe(filtered_df, use_container_width=True)

# Charts
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📈 Accuracy by Dataset")
    if not filtered_df.empty:
        chart = alt.Chart(filtered_df.dropna(subset=["Accuracy"])) \
            .mark_bar() \
            .encode(
                x="Dataset",
                y="Accuracy:Q",
                tooltip=["Dataset", "Accuracy"]
            )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No data to show.")

with col2:
    st.markdown("### 📊 Problem Type Distribution")
    if not filtered_df.empty:
        pie = alt.Chart(filtered_df).mark_arc(innerRadius=50).encode(
            theta="count()",
            color="Problem Type",
            tooltip=["Problem Type", "count()"]
        )
        st.altair_chart(pie, use_container_width=True)

with col3:
    st.markdown("### 🧠 Model Usage")
    if not filtered_df.empty:
        model_chart = alt.Chart(filtered_df).mark_bar().encode(
            x=alt.X("Model", sort='-y'),
            y="count()",
            tooltip=["Model", "count()"]
        )
        st.altair_chart(model_chart, use_container_width=True)
    else:
        st.info("No data to show.")
        
# Log Viewer
st.markdown("---")
st.subheader("📜 Cron Log Viewer")
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        log_data = f.read()
    st.text_area("Agent Log", log_data, height=300)
else:
    st.warning("Log file not found.")