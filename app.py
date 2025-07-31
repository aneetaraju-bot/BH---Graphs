import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

st.set_page_config(page_title="BH < 10% - Two Week Analysis", layout="wide")
st.title("📊 Category-wise BH < 10% (Two-Week Comparison)")

# Define the two week labels
week1 = "June 30"
week2 = "July 7"

# File uploader
uploaded_file = st.file_uploader("📁 Upload CSV with 'Category', 'Week 1', 'Week 2'", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Clean and convert
        df["Week 1"] = df["Week 1"].astype(str).str.replace("%", "").astype(float)
        df["Week 2"] = df["Week 2"].astype(str).str.replace("%", "").astype(float)

        categories = df["Category"].tolist()
        week1_vals = df["Week 1"].tolist()
        week2_vals = df["Week 2"].tolist()

        # Color zones for bars
        def get_zone_color(val):
            if val > 50:
                return 'red'
            elif val > 10:
                return 'orange'
            else:
                return 'green'

        colors1 = [get_zone_color(v) for v in week1_vals]
        colors2 = [get_zone_color(v) for v in week2_vals]

        # Plot setup
        x = np.arange(len(categories))
        width = 0.35

        fig, ax = plt.subplots(figsize=(14, 6))
        bars1 = ax.bar(x - width/2, week1_vals, width, label=week1, color=colors1)
        bars2 = ax.bar(x + width/2, week2_vals, width, label=week2, color=colors2)

        ax.set_ylabel('Percentage')
        ax.set_title('Category-wise BH < 10%')
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha="right")

        # Add % labels above each bar
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.1f}%',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=8)

        # Custom zone legend
        zone_legend = [
            Patch(facecolor='green', label='Healthy Zone'),
            Patch(facecolor='orange', label='Watch Zone'),
            Patch(facecolor='red', label='Risk Zone')
        ]
        ax.legend(handles=zone_legend, title="Batch Health Zones", loc='upper right')

        # Caption explaining the bar order
        plt.figtext(0.5, -0.05, f"(Left bar = {week1}, Right bar = {week2})", wrap=True, horizontalalignment='center', fontsize=9)

        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("📤 Please upload a CSV file with columns: Category, Week 1, Week 2.")
