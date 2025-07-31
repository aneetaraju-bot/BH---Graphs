import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

st.set_page_config(page_title="Batch Health Zones", layout="wide")
st.title("📊 Batch Health Zone Visualizer")

# --- Upload CSVs ---
st.sidebar.header("🔼 Upload CSVs")
file_below = st.sidebar.file_uploader("📉 BH < 10% CSV", type="csv")
file_above = st.sidebar.file_uploader("📈 BH > 50% CSV", type="csv")

# --- Zone Colors ---
def get_zone_color_below(current):
    if current > 30:
        return 'red'     # Risk
    elif current > 10:
        return 'orange'  # Watch
    else:
        return 'green'   # Healthy

def get_zone_color_above(current):
    if current > 50:
        return 'green'   # Healthy
    elif current > 30:
        return 'orange'  # Watch
    else:
        return 'red'     # Risk

# --- Plot Function ---
def plot_dual_bar(df, title, is_below=True):
    df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
    df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

    categories = df["Vertical"].tolist()
    last_vals = df["Last week"].tolist()
    this_vals = df["This week"].tolist()

    x = np.arange(len(categories))
    width = 0.35

    # Apply color to "This Week" bars
    zone_colors = [
        get_zone_color_below(this_vals[i]) if is_below else get_zone_color_above(this_vals[i])
        for i in range(len(categories))
    ]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width/2, last_vals, width, edgecolor='black', color='white', label='Last Week')
    ax.bar(x + width/2, this_vals, width, edgecolor='black', color=zone_colors, label='This Week')

    # Axis and layout
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.set_ylabel("Percentage of Courses")
    ax.set_title(title)

    # Zone legend (bottom right)
    zone_legend = [
        Patch(facecolor='green', edgecolor='black', label='🟩 Healthy Zone'),
        Patch(facecolor='orange', edgecolor='black', label='🟧 Watch Zone'),
        Patch(facecolor='red', edgecolor='black', label='🟥 Risk Zone'),
        Patch(facecolor='white', edgecolor='black', label='⬜ Last Week'),
        Patch(facecolor='black', edgecolor='black', label='⬛ This Week (Colored)')
    ]
    ax.legend(handles=zone_legend, loc='lower right', bbox_to_anchor=(1, -0.2), ncol=3)

    plt.tight_layout()
    st.pyplot(fig)

# --- Draw Graphs ---
if file_below:
    st.subheader("📉 BH < 10% (Low Batch Health)")
    df_below = pd.read_csv(file_below)
    df_below.rename(columns=lambda x: x.strip(), inplace=True)
    plot_dual_bar(df_below, "Zone Chart - BH < 10%", is_below=True)

if file_above:
    st.subheader("📈 BH > 50% (Healthy Batch Health)")
    df_above = pd.read_csv(file_above)
    df_above.rename(columns=lambda x: x.strip(), inplace=True)
    plot_dual_bar(df_above, "Zone Chart - BH > 50%", is_below=False)
