import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

st.set_page_config(page_title="Batch Health Zone Dashboard", layout="wide")
st.title("📊 Batch Health Dashboard")

st.sidebar.header("📂 Upload Data")
file_below = st.sidebar.file_uploader("🔻 Upload CSV for BH < 10%", type="csv")
file_above = st.sidebar.file_uploader("🔺 Upload CSV for BH > 50%", type="csv")

# -- ZONE COLOR FUNCTIONS --

def get_zone_color_below(val, avg):
    if val > avg + 5:
        return 'red'     # More risky
    elif avg - 5 <= val <= avg + 5:
        return 'orange'  # Watch zone
    else:
        return 'green'   # Healthy (less below 10%)

def get_zone_color_above(val, avg):
    if val >= avg + 5:
        return 'green'   # Healthy
    elif avg - 5 <= val <= avg + 5:
        return 'orange'  # Watch
    else:
        return 'red'     # Risk (less above 50%)

# -- PLOT FUNCTION --

def plot_chart(df, title, is_below=True):
    df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
    df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

    categories = df["Vertical"].tolist()
    last_vals = df["Last week"].tolist()
    this_vals = df["This week"].tolist()
    x = np.arange(len(categories))
    width = 0.35

    avg = np.mean(this_vals)

    # Choose color logic
    zone_colors = [
        get_zone_color_below(v, avg) if is_below else get_zone_color_above(v, avg)
        for v in this_vals
    ]

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(x - width/2, last_vals, width, color='white', edgecolor='black', label='Last Week')
    ax.bar(x + width/2, this_vals, width, color=zone_colors, edgecolor='black', label='This Week')

    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.set_ylabel("Percentage of Batches")

    label = "% Below BH 10%" if is_below else "% Above BH 50%"
    ax.set_title(f"{title} (Avg: {avg:.2f}%)")

    # Legend
    legend_elements = [
        Patch(facecolor='green', edgecolor='black', label='🟩 Healthy'),
        Patch(facecolor='orange', edgecolor='black', label='🟧 Watch Zone'),
        Patch(facecolor='red', edgecolor='black', label='🟥 Risk'),
        Patch(facecolor='white', edgecolor='black', label='⬜ Last Week'),
        Patch(facecolor='black', edgecolor='black', label='⬛ This Week')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))

    st.pyplot(fig)

# -- BH < 10% --
if file_below:
    st.subheader("📉 Zone Chart for Batches Below BH 10%")
    df_below = pd.read_csv(file_below)
    df_below.rename(columns=lambda x: x.strip(), inplace=True)
    plot_chart(df_below, "Zone Classification Based on % of Batches Below BH 10%", is_below=True)

# -- BH > 50% --
if file_above:
    st.subheader("📈 Zone Chart for Batches Above BH 50%")
    df_above = pd.read_csv(file_above)
    df_above.rename(columns=lambda x: x.strip(), inplace=True)
    plot_chart(df_above, "Zone Classification Based on % of Batches Above BH 50%", is_below=False)
