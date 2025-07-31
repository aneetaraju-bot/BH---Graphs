import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

st.set_page_config(page_title="Batch Health Comparison", layout="centered")
st.title("📊 Vertical-wise BH < 10% Comparison")

# Define the week dates (you can make these dynamic if needed)
last_week_date = "June 24"
this_week_date = "June 30"

# Upload CSV
uploaded_file = st.file_uploader("📁 Upload CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Validate expected format
    try:
        categories = df["Category"].tolist()
        last_week_below_10 = df["Last week"].tolist()
        this_week_below_10 = df["This week"].tolist()

        x = np.arange(len(categories))
        wi
