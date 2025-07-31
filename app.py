import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

st.set_page_config(page_title="Batch Health Zones", layout="wide")
st.title("📊 Batch Health Zone Visualizer")

# --- Upload ---
st.sidebar.header("🔼 Upload CSVs")
file_below = st.sidebar.file_uploader("📉 BH < 10% CSV", type="csv")
file_above = st.sidebar.file_uploader("📈 BH > 50% CSV", type="csv")

# --- Absolute Zone Color Based on "This Week" % ---
def get_zone_color_below(current):
    if current > 30:
        return 'red'     # High risk
    elif current > 10:
        return 'orange'  # Caution
    else:
        return 'green'   # Healthy

def get_zone_color_above(current):
    if current > 50:
        return 'green'   # Healthy
    elif current > 30:
        return 'orange'  # Moderate
    else:
        return 'red'     # Risk

# --- Graph function ---
def plot_dual_bar(df, title, is_below=True):
    df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
    df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

    categories = df["Vertical"].tolist()
    last_vals = df["Last week"].tolist()
    this_vals = df["This week"].tolist()

    x = np.arange(len(categories))
    width = 0.35

    zone_colors = [
        get_zone_color_below(this_vals[i]) if is_below else get_zone_color_above(this_vals[i])
        for i in range(len(categories))
    ]

    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot both bars, no gray fill
    ax.bar(x - width/2, last_vals, width, edgecolor='black', label='Last Week', color='white')
    ax.bar(x + width/2, this_vals, width, color=zone_colors, edgecolor='black', label='This Week')

    # Axes and layout
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.set_ylabel("Percentage of Courses")
    ax.set_title(title)

    # Custom Legend
    legend_elements = [
        Patch(facecolor='green', edgecolor='black', label='🟩 Healthy Zone (<10%)'),
        Patch(facecolor='orange', edgecolor='black', label='🟧 Watch Zone (10%-30%)'),
        Patch(facecolor='red', edgecolor='black', label='🟥 Risk Zone (>30%)'),
        Patch(facecolor='white', edgecolor='black', label='⬜ Last Week'),
        Patch(facecolor='black', edgecolor='black', label='⬛ This Week (Color Coded)')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    st.pyplot(fig)

# --- Render charts ---
if file_below:
    st.subheader("📉 BH < 10% (Low Batch Health)")
    df_below = pd.read_csv(file_below)
    df_below.rename(columns=lambda x: x.strip(), inplace=True)
    plot_dual_bar(df_below, "Batch Health < 10% - Zone View", is_below=True)

if file_above:
    st.subheader("📈 BH > 50% (High Batch Health)")
    df_above = pd.read_csv(file_above)
    df_above.rename(columns=lambda x: x.strip(), inplace=True)
    plot_dual_bar(df_above, "Batch Health > 50% - Zone View", is_below=False)
