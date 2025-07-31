import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

st.set_page_config(page_title="BH < 10% - Week Comparison", layout="wide")
st.title("📊 Batch Health < 10% - Last Week vs This Week")

# Upload CSV
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

        x = np.arange(len(categories))
        width = 0.35

        # Zone color logic
        def get_zone_color(val):
            if val >= 50:
                return "red"
            elif val >= 10:
                return "orange"
            else:
                return "green"

        colors_last = [get_zone_color(val) for val in last_vals]
        colors_this = [get_zone_color(val) for val in this_vals]

        # Trend arrow
        def get_change_arrow(this, last):
            if this < last:
                return "↓"
            elif this > last:
                return "↑"
            else:
                return "→"

        # Label showing % change
        def get_change_label(this, last):
            diff = this - last
            symbol = get_change_arrow(this, last)
            return f"{symbol} {abs(diff):.2f}%"

        change_labels = [get_change_label(this, last) for this, last in zip(this_vals, last_vals)]

        # Plotting
        fig, ax = plt.subplots(figsize=(14, 6))
        bars1 = ax.bar(x - width/2, last_vals, width, label="Last Week", color=colors_last)
        bars2 = ax.bar(x + width/2, this_vals, width, label="This Week", color=colors_this)

        ax.set_ylabel("BH < 10%")
        ax.set_title("📉 BH < 10% Comparison - Last Week vs This Week")
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha="right")

        # Annotate only THIS WEEK bars with % + trend
        for i, bar in enumerate(bars2):
            height = bar.get_height()
            ax.annotate(f'{height:.2f}%\n{change_labels[i]}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)

        # Legends
        zone_legend = [
            Patch(color='green', label='Healthy Zone (<10%)'),
            Patch(color='orange', label='Watch Zone (10–50%)'),
            Patch(color='red', label='Risk Zone (50%+)')
        ]
        ax.legend(handles=zone_legend, title="Zone", loc="upper left")
        ax.legend(loc="upper right", title="Week")

        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.info("📤 Please upload a CSV file with columns: Category, Last week, This week.")
