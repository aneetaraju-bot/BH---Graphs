import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

st.set_page_config(page_title="Batch Health Comparison", layout="centered")
st.title("📊 Vertical-wise BH < 10% Comparison")

# Define the week labels
last_week_date = "June 24"
this_week_date = "June 30"

# File uploader
uploaded_file = st.file_uploader("📁 Upload CSV with 'Category', 'Last week', 'This week' columns", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Clean % symbols and convert to float
        df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
        df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

        # Extract data
        categories = df["Category"].tolist()
        last_week_below_10 = df["Last week"].tolist()
        this_week_below_10 = df["This week"].tolist()

        # X positions
        x = np.arange(len(categories))
        width = 0.35

        # Color logic
        def get_zone_color(val):
            if val > 50:
                return 'red'
            elif val > 10:
                return 'orange'
            else:
                return 'green'

        last_colors = [get_zone_color(v) for v in last_week_below_10]
        this_colors = [get_zone_color(v) for v in this_week_below_10]

        # Plot
        fig, ax = plt.subplots(figsize=(12, 6))
        bars1 = ax.bar(x - width/2, last_week_below_10, width, color=last_colors)
        bars2 = ax.bar(x + width/2, this_week_below_10, width, color=this_colors)

        ax.set_ylabel('Percentage')
        ax.set_title('Vertical-wise BH < 10%')
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45)

        # Add % and date labels on bars
        def add_labels(bars, date_label):
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.2f}%\n({date_label})',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 5),
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=9)

        add_labels(bars1, last_week_date)
        add_labels(bars2, this_week_date)

        # Legend
        ax.legend(handles=[
            Patch(facecolor='green', label='Healthy (<10%)'),
            Patch(facecolor='orange', label='Watch Zone (10–50%)'),
            Patch(facecolor='red', label='Risk Zone (>50%)')
        ], loc='upper right')

        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("📤 Please upload a CSV file with columns: Category, Last week, This week.")

