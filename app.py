import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

st.set_page_config(page_title="BH < 10% Trend Analysis", layout="centered")
st.title("📊 BH < 10% - Last Week vs This Week")

# File uploader
uploaded_file = st.file_uploader("📁 Upload CSV with 'Category', 'Last week', 'This week' columns", type=["csv"])

if uploaded_file:
    try:
        # Read and clean data
        df = pd.read_csv(uploaded_file)
        df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
        df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

        # Extract columns
        categories = df["Category"].tolist()
        last_vals = df["Last week"].tolist()
        this_vals = df["This week"].tolist()

        # Trend-based coloring (↓ improved, ↑ declined, → no change)
        def get_trend_color(this, last):
            if this < last:
                return "green"
            elif this > last:
                return "red"
            else:
                return "gold"

        colors = [get_trend_color(this, last) for this, last in zip(this_vals, last_vals)]

        # Plot
        x = np.arange(len(categories))
        width = 0.6
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(x, this_vals, width, color=colors)

        ax.set_ylabel("BH < 10%")
        ax.set_title("BH < 10% - This Week Compared to Last Week")
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha="right")

        # Add % and arrow indicators
        for i, bar in enumerate(bars):
            height = bar.get_height()
            delta = this_vals[i] - last_vals[i]
            symbol = "↓" if delta < 0 else "↑" if delta > 0 else "→"
            ax.annotate(f"{height:.2f}%\n{symbol}",
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=9)

        # Custom legend
        ax.legend(handles=[
            Patch(color='green', label='Improved (↓)'),
            Patch(color='red', label='Declined (↑)'),
            Patch(color='gold', label='No Change (→)')
        ], loc='upper right')

        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("📤 Please upload a CSV file with columns: Category, Last week, This week.")
