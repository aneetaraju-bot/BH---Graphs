import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# Page config
st.set_page_config(page_title="Batch Health Comparison", layout="wide")
st.title("📊 Batch Health Comparison by Vertical")

# Upload both CSVs
st.subheader("📁 Upload CSV for BH < 10%")
file_below10 = st.file_uploader("Upload BH < 10% CSV", type=["csv"], key="below10")

st.subheader("📁 Upload CSV for BH > 50%")
file_above50 = st.file_uploader("Upload BH > 50% CSV", type=["csv"], key="above50")

# Plot function
def plot_bh_graph(df, title):
    df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
    df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

    verticals = df["Vertical"].tolist()
    last_vals = df["Last week"].tolist()
    this_vals = df["This week"].tolist()

    x = np.arange(len(verticals))
    width = 0.35

    # Zone color function
    def get_zone_color(val):
        if val >= 50:
            return "red"
        elif val >= 10:
            return "orange"
        else:
            return "green"

    colors_last = [get_zone_color(val) for val in last_vals]
    colors_this = [get_zone_color(val) for val in this_vals]

    fig, ax = plt.subplots(figsize=(max(12, len(verticals) * 1), 7))

    # Bars
    ax.bar(x - width/2, last_vals, width, color=colors_last, edgecolor='blue', linewidth=2)
    ax.bar(x + width/2, this_vals, width, color=colors_this, edgecolor='gold', linewidth=2)

    ax.set_ylabel("Percentage")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(verticals, rotation=45, ha="right")

    # Labels on bars
    for i in range(len(verticals)):
        ax.text(x[i] - width/2, last_vals[i] + 1, f"{last_vals[i]:.2f}", ha='center', fontsize=9)
        ax.text(x[i] + width/2, this_vals[i] + 1, f"{this_vals[i]:.2f}", ha='center', fontsize=9)

    # Legends
    zone_legend = [
        Patch(color='green', label='Healthy Zone (<10%)'),
        Patch(color='orange', label='Watch Zone (10–50%)'),
        Patch(color='red', label='Risk Zone (50%+)')
    ]
    week_legend = [
        Patch(facecolor='white', edgecolor='blue', linewidth=2, label='⬅️ Last Week'),
        Patch(facecolor='white', edgecolor='gold', linewidth=2, label='➡️ This Week')
    ]

    ax.legend(
        handles=zone_legend + week_legend,
        title="Legend",
        loc='upper right',
        bbox_to_anchor=(1, 1),
        frameon=True
    )

    plt.tight_layout()
    return fig

# Show charts if files uploaded
if file_below10:
    try:
        st.markdown("### 📉 BH Below 10% Analysis")
        df1 = pd.read_csv(file_below10)
        fig1 = plot_bh_graph(df1, "BH < 10% - Vertical-wise Comparison")
        st.pyplot(fig1)
    except Exception as e:
        st.error(f"Error reading BH < 10% file: {e}")

if file_above50:
    try:
        st.markdown("### 📈 BH Above 50% Analysis")
        df2 = pd.read_csv(file_above50)
        fig2 = plot_bh_graph(df2, "BH > 50% - Vertical-wise Comparison")
        st.pyplot(fig2)
    except Exception as e:
        st.error(f"Error reading BH > 50% file: {e}")
