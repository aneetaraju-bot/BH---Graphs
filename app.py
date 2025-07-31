import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

st.set_page_config(page_title="Batch Health Zone Charts", layout="wide")
st.title("📊 Batch Health Zone Visualizer")

# ---- Upload Two CSVs ----
st.sidebar.header("📂 Upload Data")
file_below = st.sidebar.file_uploader("📉 BH < 10% CSV", type="csv")
file_above = st.sidebar.file_uploader("📈 BH > 50% CSV", type="csv")

# ---- Zone Logic Functions ----
def get_zone_color_below(current):
    if current > 30:
        return 'red'
    elif current > 10:
        return 'orange'
    else:
        return 'green'

def get_zone_color_above(current):
    if current >= 75:
        return 'green'
    elif current >= 50:
        return 'orange'
    else:
        return 'red'

# ---- Chart Generator ----
def plot_bh_chart(df, title, is_below=True):
    df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
    df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

    categories = df["Vertical"].tolist()
    last_vals = df["Last week"].tolist()
    this_vals = df["This week"].tolist()

    x = np.arange(len(categories))
    width = 0.35

    # Assign zone colors based on this week %
    zone_colors = [
        get_zone_color_below(this_vals[i]) if is_below else get_zone_color_above(this_vals[i])
        for i in range(len(categories))
    ]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width/2, last_vals, width, edgecolor='black', color='white', label='Last Week')
    ax.bar(x + width/2, this_vals, width, edgecolor='black', color=zone_colors, label='This Week')

    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ylabel = "Percentage of Batches Below BH 10%" if is_below else "Percentage of Batches Above BH 50%"
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    # Legend inside top right corner
    legend_elements = [
        Patch(facecolor='green', edgecolor='black', label='🟩 Healthy Zone'),
        Patch(facecolor='orange', edgecolor='black', label='🟧 Watch Zone'),
        Patch(facecolor='red', edgecolor='black', label='🟥 Risk Zone'),
        Patch(facecolor='white', edgecolor='black', label='⬜ Last Week'),
        Patch(facecolor='black', edgecolor='black', label='⬛ This Week (Color-Coded)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))

    st.pyplot(fig)

# ---- Render Charts ----
if file_below:
    st.subheader("📉 Chart: Batches with BH < 10%")
    df_below = pd.read_csv(file_below)
    df_below.rename(columns=lambda x: x.strip(), inplace=True)
    plot_bh_chart(df_below, "Zone Chart - % of Batches Below BH 10%", is_below=True)

if file_above:
    st.subheader("📈 Chart: Batches with BH > 50%")
    df_above = pd.read_csv(file_above)
    df_above.rename(columns=lambda x: x.strip(), inplace=True)
    plot_bh_chart(df_above, "Zone Chart - % of Batches Above BH 50%", is_below=False)
