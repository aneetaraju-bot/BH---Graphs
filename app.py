import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

st.set_page_config(page_title="BH < 10% Category Analysis", layout="wide")
st.title("📊 Batch Health < 10% - Zone + Change Analysis")

uploaded_file = st.file_uploader("📁 Upload CSV with 'Category', 'Last week', 'This week' columns", type=["csv"])

if uploaded_file:
    try:
        # Load and clean
        df = pd.read_csv(uploaded_file)
        df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
        df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

        categories = df["Category"].tolist()
        last_vals = df["Last week"].tolist()
        this_vals = df["This week"].tolist()

        # Zone-based color (based on THIS week)
        def get_zone_color(val):
            if val >= 50:
                return "red"     # Risk zone
            elif val >= 10:
                return "orange"  # Watch zone
            else:
                return "green"   # Healthy

        zone_colors = [get_zone_color(v) for v in this_vals]

        # Change arrow
        def get_trend_arrow(this, last):
            if this < last:
                return "↓"
            elif this > last:
                return "↑"
            else:
                return "→"

        # Change percentage
        def get_change_label(this, last):
            diff = this - last
            symbol = get_trend_arrow(this, last)
            return f"{symbol} {abs(diff):.2f}%" if diff != 0 else f"{symbol} 0.00%"

        change_labels = [get_change_label(this, last) for this, last in zip(this_vals, last_vals)]

        # Plotting
        x = np.arange(len(categories))
        width = 0.6

        fig, ax = plt.subplots(figsize=(14, 6))
        bars = ax.bar(x, this_vals, width, color=zone_colors)

        ax.set_ylabel("BH < 10%")
        ax.set_title("BH < 10% (This Week) with Zone & Week-over-Week Change")
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha="right")

        # Annotate bars with % and trend
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.annotate(f'{height:.2f}%\n{change_labels[i]}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)

        # Legends
        ax.legend(handles=[
            Patch(color='green', label='Healthy Zone (<10%)'),
            Patch(color='orange', label='Watch Zone (10–50%)'),
            Patch(color='red', label='Risk Zone (50%+)')
        ], title="Current Week Zone", loc='upper right')

        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

else:
    st.info("📤 Please upload a CSV file with columns: Category, Last week, This week.")
