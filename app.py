import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# Streamlit page config
st.set_page_config(page_title="Batch Health Risk Analysis", layout="wide")
st.title("📊 Batch Health Tracker: Risk & Healthy Zone (% of Courses)")

# Upload inputs
st.subheader("🔻 Upload BH < 10% CSV")
file_below10 = st.file_uploader("Upload % of batches in BH < 10", type=["csv"], key="below10")

st.subheader("🔺 Upload BH > 50% CSV")
file_above50 = st.file_uploader("Upload % of batches in BH > 50", type=["csv"], key="above50")

# Trend + zone coloring logic
def get_below10_trend(last, current):
    diff = current - last
    if diff > 5:
        return "↑↑", "Strong Risk", "red"
    elif diff > 1:
        return "↑", "Mild Risk", "red"
    elif diff < -5:
        return "↓↓", "Strong Healthy", "green"
    elif diff < -1:
        return "↓", "Mild Healthy", "green"
    else:
        return "→", "Watch", "orange"

def get_above50_trend(last, current):
    diff = current - last
    if diff > 5:
        return "↑↑", "Strong Healthy", "green"
    elif diff > 1:
        return "↑", "Mild Healthy", "green"
    elif diff < -5:
        return "↓↓", "Strong Risk", "red"
    elif diff < -1:
        return "↓", "Mild Risk", "red"
    else:
        return "→", "Watch", "orange"

# Graph plotter
def plot_graph(df, title, is_below10=True):
    df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
    df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

    categories = df["Vertical"].tolist()
    last_vals = df["Last week"].tolist()
    this_vals = df["This week"].tolist()

    x = np.arange(len(categories))
    width = 0.35

    arrows, meanings, zone_colors = [], [], []
    for i in range(len(categories)):
        if is_below10:
            arrow, meaning, color = get_below10_trend(last_vals[i], this_vals[i])
        else:
            arrow, meaning, color = get_above50_trend(last_vals[i], this_vals[i])
        arrows.append(arrow)
        meanings.append(meaning)
        zone_colors.append(color)

    fig, ax = plt.subplots(figsize=(max(12, len(categories) * 1.2), 7))

    # Bar chart
    ax.bar(x - width/2, last_vals, width, edgecolor='blue', facecolor='white', linewidth=2)
    ax.bar(x + width/2, this_vals, width, color=zone_colors, edgecolor='black', linewidth=2)

    ax.set_ylabel("% of Courses")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha="right")

    for i in range(len(categories)):
        ax.text(x[i] - width/2, last_vals[i] + 1, f"{last_vals[i]:.2f}", ha='center', fontsize=9)
        ax.text(x[i] + width/2, this_vals[i] + 1, f"{this_vals[i]:.2f} {arrows[i]}", ha='center', fontsize=9, color=zone_colors[i])

    # Legends
    zone_legend = [
        Patch(color='green', label='🟩 Healthy Zone'),
        Patch(color='orange', label='🟧 Watch Zone'),
        Patch(color='red', label='🟥 Risk Zone')
    ]
    trend_legend = [
        Patch(facecolor='white', edgecolor='black', linewidth=1, label='⬅️ Last Week'),
        Patch(facecolor='white', edgecolor='black', label='➡️ This Week')
    ]

    ax.legend(handles=zone_legend + trend_legend, title="Legend", loc='upper right', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    return fig

# Display charts
if file_below10:
    try:
        st.markdown("### 🔻 % of Courses in BH < 10%")
        df1 = pd.read_csv(file_below10)
        df1.rename(columns=lambda x: x.strip(), inplace=True)
        fig1 = plot_graph(df1, "Batch Health Below 10% Trend & Zones", is_below10=True)
        st.pyplot(fig1)
    except Exception as e:
        st.error(f"Error processing BH < 10%: {e}")

if file_above50:
    try:
        st.markdown("### 🔺 % of Courses in BH > 50%")
        df2 = pd.read_csv(file_above50)
        df2.rename(columns=lambda x: x.strip(), inplace=True)
        fig2 = plot_graph(df2, "Batch Health Above 50% Trend & Zones", is_below10=False)
        st.pyplot(fig2)
    except Exception as e:
        st.error(f"Error processing BH > 50%: {e}")
