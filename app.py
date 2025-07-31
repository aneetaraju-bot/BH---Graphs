import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

st.set_page_config(page_title="BH < 10% Trend Analysis", layout="centered")
st.title("📊 BH < 10% - Week-over-Week Trend")

# Define the week labels
last_week_date = "June 24"
this_week_date = "June 30"

# File uploader
uploaded_file = st.file_uploader("📁 Upload CSV with 'Category', 'Last week', 'This week' columns", type=["csv"])

if uploaded_file:
    try:
        # Load CSV
        df = pd.read_csv(uploaded_file)

        # Clean percentage symbols and convert to float
        df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
        df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

        # Extract data
        categories = df["Category"].tolist()
        last_week_vals = df["Last week"].tolist()
        this_week_vals = df["This week"].tolist()

        # Determine color based on trend
        def get_trend_color(this_val, last_val):
            if this_val < last_val:
                return 'green'   # Improved
            elif this_val > last_val:
                return 'red'     # Declined
            else:
                return 'gold'    # No change

        trend_colors = [get_trend_color(this, last) for this, last in zip(this_week_vals, last_week_vals)]

        # Plotting this week's values
        x = np.arange(len(categories))
        width = 0.6

        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(x, this_week_vals, width, color=trend_colors)

        ax.set_ylabel('BH < 10%')
        ax.set_title(f'📉 BH < 10% - {this_week_date} vs {last_week_date}')
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45)

        # Add % and trend symbols on top of bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            change = this_week_vals[i] - last_week_vals[i]
            trend = "↓" if change < 0 else "↑" if change > 0 else "→"
            ax.annotate(f'{height:.2f}%\n{trend}',
                        xy=(bar.get_x() + bar.get_width()/2, height),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)

        # Add legend
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
