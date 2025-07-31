import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# Page config
st.set_page_config(page_title="Category-wise BH < 10%", layout="wide")
st.title("📊 Category-wise BH < 10% Comparison")

uploaded_file = st.file_uploader("📁 Upload CSV with 'Category', 'Last week', 'This week'", type=["csv"])

if uploaded_file:
    try:
        # Load and process
        df = pd.read_csv(uploaded_file)
        df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
        df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

        categories = df["Category"].tolist()
        last_vals = df["Last week"].tolist()
        this_vals = df["This week"].tolist()

        x = np.arange(len(categories))
        width = 0.35

        # Color zones
        def get_zone_color(val):
            if val >= 50:
                return "red"
            elif val >= 10:
                return "orange"
            else:
                return "green"

        colors_last = [get_zone_color(val) for val in last_vals]
        colors_this = [get_zone_color(val) for val in this_vals]

        # Plot setup
        fig, ax = plt.subplots(figsize=(max(12, len(categories) * 1), 7))

        bars1 = ax.bar(x - width/2, last_vals, width, color=colors_last, edgecolor='blue', linewidth=2)
        bars2 = ax.bar(x + width/2, this_vals, width, color=colors_this, edgecolor='gold', linewidth=2)

        # Axes and title
        ax.set_ylabel("Percentage")
        ax.set_title("Category-wise BH < 10%")
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha="right")

        # Add value labels on top
        for i in range(len(categories)):
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

        # Combine both legends
        legend1 = ax.legend(handles=zone_legend, title="Zone Color", loc="upper left")
        ax.add_artist(legend1)
        ax.legend(handles=week_legend, title="Week", loc="upper right")

        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("📤 Please upload a CSV with columns: Category, Last week, This week.")
