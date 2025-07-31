import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

st.set_page_config(page_title="Category-wise BH < 10%", layout="wide")
st.title("📊 Category-wise BH < 10% Comparison")

uploaded_file = st.file_uploader("📁 Upload CSV with 'Category', 'Last week', 'This week'", type=["csv"])

if uploaded_file:
    try:
        # Load and clean
        df = pd.read_csv(uploaded_file)
        df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
        df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

        categories = df["Category"].tolist()
        last_vals = df["Last week"].tolist()
        this_vals = df["This week"].tolist()

        x = np.arange(len(categories))
        width = 0.35

        # Zone coloring
        def get_color(val):
            if val >= 50:
                return "red"
            elif val >= 10:
                return "orange"
            else:
                return "green"

        colors_last = [get_color(val) for val in last_vals]
        colors_this = [get_color(val) for val in this_vals]

        # Plot
        fig, ax = plt.subplots(figsize=(16, 7))
        ax.bar(x - width/2, last_vals, width, color=colors_last)
        ax.bar(x + width/2, this_vals, width, color=colors_this)

        ax.set_ylabel("Percentage")
        ax.set_title("Category-wise BH < 10%")
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha="right")

        # Add custom text labels on top of bars
        for i in range(len(categories)):
            ax.text(x[i] - width/2, last_vals[i] + 1, f"{last_vals[i]:.2f}", ha='center', fontsize=9)
            ax.text(x[i] + width/2, this_vals[i] + 1, f"{this_vals[i]:.2f}", ha='center', fontsize=9)

        # Only show zone color meaning (no week labels)
        zone_legend = [
            Patch(color='green', label='🟩 Healthy Zone (<10%)'),
            Patch(color='orange', label='🟧 Watch Zone (10–50%)'),
            Patch(color='red', label='🟥 Risk Zone (50%+)')
        ]
        ax.legend(handles=zone_legend, title="Batch Health Zones", loc="upper right")

        # Bottom caption showing bar position meaning
        plt.figtext(0.5, 0.01, "Left bar = Last Week | Right bar = This Week", ha="center", fontsize=10)

        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("📤 Please upload a CSV with columns: Category, Last week, This week.")
