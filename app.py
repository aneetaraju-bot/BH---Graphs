import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# Streamlit page setup
st.set_page_config(page_title="Batch Health Trend Zones", layout="wide")
st.title("📊 Batch Health Risk & Zone Tracker by Vertical")

# Upload files
st.subheader("📁 Upload CSV for BH < 10%")
file_below10 = st.file_uploader("Upload BH < 10% CSV", type=["csv"], key="below10")

st.subheader("📁 Upload CSV for BH > 50%")
file_above50 = st.file_uploader("Upload BH > 50% CSV", type=["csv"], key="above50")

# Function for determining zone color based on trend
def get_zone_color_below10(last, current):
    if current > last:
        return "red"    # BH < 10% increasing = risk
    elif current < last:
        return "green"  # BH < 10% decreasing = improvement
    else:
        return "orange" # No change

def get_zone_color_above50(last, current):
    if current > last:
        return "green"  # BH > 50% increasing = improvement
    elif current < last:
        return "red"    # BH > 50% decreasing = risk
    else:
        return "orange" # No change

# Main plot function
def plot_graph(df, title, bh_type):
    df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
    df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

    verticals = df["Vertical"].tolist()
    last_vals = df["Last week"].tolist()
    this_vals = df["This week"].tolist()
    x = np.arange(len(verticals))
    width = 0.35

    # Color each bar based on trend
    if bh_type == "below10":
        colors_this = [get_zone_color_below10(last_vals[i], this_vals[i]) for i in range(len(verticals))]
        colors_last = colors_this  # Keep same color logic for comparison
    else:
        colors_this = [get_zone_color_above50(last_vals[i], this_vals[i]) for i in range(len(verticals))]
        colors_last = colors_this

    fig, ax = plt.subplots(figsize=(max(12, len(verticals) * 1.2), 7))

    ax.bar(x - width/2, last_vals, width, color=colors_last, edgecolor='blue', linewidth=2)
    ax.bar(x + width/2, this_vals, width, color=colors_this, edgecolor='gold', linewidth=2)

    ax.set_ylabel("Percentage")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(verticals, rotation=45, ha="right")

    # Add value and arrow with improvement color
    for i in range(len(verticals)):
        diff = this_vals[i] - last_vals[i]
        improving = (diff < 0 and bh_type == "below10") or (diff > 0 and bh_type == "above50")
        arrow = "↑" if diff > 0 else "↓"
        arrow_color = "green" if improving else "red"

        ax.text(x[i] - width/2, last_vals[i] + 1, f"{last_vals[i]:.2f}", ha='center', fontsize=9)
        ax.text(x[i] + width/2, this_vals[i] + 1, f"{this_vals[i]:.2f} {arrow}", ha='center', fontsize=9, color=arrow_color)

    # Legend based on zone logic
    zone_legend = [
        Patch(color='green', label='🟩 Healthy Zone'),
        Patch(color='orange', label='🟧 Watch Zone'),
        Patch(color='red', label='🟥 Risk Zone')
    ]
    week_legend = [
        Patch(facecolor='white', edgecolor='blue', linewidth=2, label='⬅️ Last Week'),
        Patch(facecolor='white', edgecolor='gold', linewidth=2, label='➡️ This Week')
    ]

    ax.legend(handles=zone_legend + week_legend,
              title="Legend",
              loc='upper right',
              bbox_to_anchor=(1, 1),
              frameon=True)

    plt.tight_layout()
    return fig

# Render charts
if file_below10:
    try:
        st.markdown("### 🔻 BH Below 10% (Increasing is Risk)")
        df1 = pd.read_csv(file_below10)
        fig1 = plot_graph(df1, "BH < 10% - Zone Analysis", "below10")
        st.pyplot(fig1)
    except Exception as e:
        st.error(f"Error reading BH < 10% CSV: {e}")

if file_above50:
    try:
        st.markdown("### 🔺 BH Above 50% (Increasing is Healthy)")
        df2 = pd.read_csv(file_above50)
        fig2 = plot_graph(df2, "BH > 50% - Zone Analysis", "above50")
        st.pyplot(fig2)
    except Exception as e:
        st.error(f"Error reading BH > 50% CSV: {e}")
