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

        # Zone-based color for both weeks
        def get_zone_color(val):
            if val >= 50:
                return "red"
            elif val >= 10:
                return "orange"
            else:
                return "green"

        colors_last = [get_zone_color(val) for val in last_vals]
        colors_this = [get_zone_color(val) for val in this_vals]

        # Change indicators
        def get_change_arrow(this, last):
            if this < last:
                return "↓"
