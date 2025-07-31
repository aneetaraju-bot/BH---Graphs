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
        # Load and clean data
        df = pd.read_csv(uploaded_file)
        df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
        df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

        categories = df["Category"].tolist()
        last_vals = df["Last week"].tolist()
        this_vals = df["This week"].tolist()

        # Each category gets two bars → double x positions
        total_bars = len(categories) * 2
        x = np.arange(total_bars)
        width = 0.8

        # Flattened data and labels
        values = []
        colors = []
        x_labels = []

        def get_color(val):
            if val >= 50:
                return "red"
            elif val >= 10:
                return "orange"
            else:
                return "green"

        for i in range(len(categories)):
            # Left bar = last week
            values.append(last_vals[i])
            colors.append(get_color(last_vals[i]))
            x_labels.append(f"{categories[i]}\nLast Week")

            # Right bar = this week
            values.append(this_vals[i])
            colors.append(get_color(this_vals[i]))
            x_labels.append(f"{categories[i]}\nThis Week")

        # Plot
        fig, ax = plt.subplots(figsize=(max(10, len(x) * 0.6), 7))
        bars = ax.bar(x, values, width=width * 0.9, color=colors)

        # Add value labels above bars
        for idx, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 1, f"{values[idx]:.2f}", ha='center', fontsize=9)

        ax.set_ylabel("Percentage")
        ax.set_title("Category-wise BH < 10%")
        ax.set_xticks(x)
        ax.set_xticklabels(x_labels, rotation=45, ha="right")

        # Color zone legend
        zone_legend = [
            Patch(color='green', label='🟩 Healthy Zone (<10%)'),
            Patch(color='orange', label='🟧 Watch Zone (10–50%)'),
            Patch(color='red', label='🟥 Risk Zone (50%+)')
        ]
        ax.legend(handles=zone_legend, title="Batch Health Zones", loc="upper right")

        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("📤 Please upload a CSV with columns: Category, Last week, This week.")
