import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# Streamlit config
st.set_page_config(page_title="Category-wise BH < 10%", layout="wide")
st.title("📊 Category-wise BH < 10% Comparison")

# File uploader
uploaded_file = st.file_uploader("📁 Upload CSV with 'Category', 'Last week', 'This week'", type=["csv"])

if uploaded_file:
    try:
        # Load and preprocess
        df = pd.read_csv(uploaded_file)
        df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
        df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

        categories = df["Category"].tolist()
        last_vals = df["Last week"].tolist()
        this_vals = df["This week"].tolist()

        x = np.arange(len(categories))
        width = 0.35

        # Color zone function
        def get_color(val):
            if val >= 50:
                return "red"
            elif val >= 10:
                return "orange"
            else:
                return "green"

        colors_last = [get_color(val) for val in last_vals]
        colors_this = [get_color(val) for val in this_vals]

        # Plotting
        fig, ax = plt.subplots(figsize=(16, 7))
        ax.bar(x - width/2, last_vals, width, label='Last Week', color=colors_last)
        ax.bar(x + width/2, this_vals, width, label='This Week', color=colors_this)

        ax.set_ylabel("Percentage")
        ax.set_title("Category-wise BH < 10%")
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha="right")

        # Color zone legend
        zone_legend = [
            Patch(facecolor='green', label='🟩 Healthy Zone (<10%)'),
            Patch(facecolor='orange', label='🟧 Watch Zone (10–50%)'),
            Patch(facecolor='red', label='🟥 Risk Zone (50%+)')
        ]
        ax.legend(handles=zone_legend, title="Batch Health Zones", loc="upper left")
        ax.legend(title="Week", loc="upper right")

        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("📤 Please upload a CSV with columns: Category, Last week, This week.")
