import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

st.set_page_config(page_title="Batch Health Zones", layout="wide")
st.title("📊 Batch Health Visualizer (Zone-Based)")

# --- Upload ---
st.sidebar.header("🔼 Upload CSVs")
file_below = st.sidebar.file_uploader("📉 BH < 10% CSV", type="csv")
file_above = st.sidebar.file_uploader("📈 BH > 50% CSV", type="csv")

# --- Zone color functions ---
def get_zone_color_below(last, current):
    diff = current - last
    if diff > 1:
        return 'red'
    elif diff < -1:
        return 'green'
    else:
        return 'orange'

def get_zone_color_above(last, current):
    diff = current - last
    if diff > 1:
        return 'green'
    elif diff < -1:
        return 'red'
    else:
        return 'orange'

# --- Graph function ---
def plot_dual_bar(df, title, is_below=True):
    df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
    df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

    categories = df["Vertical"].tolist()
    last_vals = df["Last week"].tolist()
    this_vals = df["This week"].tolist()

    x = np.arange(len(categories))
    width = 0.35

    zone_colors = []
    for i in range(len(categories)):
        if is_below:
            zone_colors.append(get_zone_color_below(last_vals[i], this_vals[i]))
        else:
            zone_colors.append(get_zone_color_above(last_vals[i], this_vals[i]))

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width/2, last_vals, width, label='Last Week', color='gray', edgecolor='black')
    ax.bar(x + width/2, this_vals, width, label='This Week', color=zone_colors, edgecolor='black')

    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.set_ylabel("Percentage of Courses")
    ax.set_title(title)

    legend_elements = [
        Patch(facecolor='green', edgecolor='black', label='🟩 Healthy Zone'),
        Patch(facecolor='orange', edgecolor='black', label='🟧 Watch Zone'),
        Patch(facecolor='red', edgecolor='black', label='🟥 Risk Zone'),
        Patch(facecolor='gray', edgecolor='black', label='⬛ Last Week'),
        Patch(facecolor='white', edgecolor='black', label='⬜ This Week (Color Coded)')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    st.pyplot(fig)

# --- Render charts ---
if file_below:
    st.subheader("📉 BH < 10% - Risk Zone Chart")
    df_below = pd.read_csv(file_below)
    df_below.rename(columns=lambda x: x.strip(), inplace=True)
    plot_dual_bar(df_below, "BH < 10% Zone Analysis", is_below=True)

if file_above:
    st.subheader("📈 BH > 50% - Healthy Zone Chart")
    df_above = pd.read_csv(file_above)
    df_above.rename(columns=lambda x: x.strip(), inplace=True)
    plot_dual_bar(df_above, "BH > 50% Zone Analysis", is_below=False)
