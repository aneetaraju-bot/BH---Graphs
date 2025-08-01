import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

st.set_page_config(page_title="Batch Health Zone Dashboard", layout="wide")
st.title("📊 Batch Health Zone Dashboard – 4 Graphs + Zone Tracking")

# Sidebar: Upload CSV files
st.sidebar.header("📂 Upload CSV Files")
file_v_below = st.sidebar.file_uploader("1️⃣ Vertical-wise BH < 10%", type="csv")
file_v_above = st.sidebar.file_uploader("2️⃣ Vertical-wise BH > 50%", type="csv")
file_c_below = st.sidebar.file_uploader("3️⃣ Category-wise BH < 10%", type="csv")
file_c_above = st.sidebar.file_uploader("4️⃣ Category-wise BH > 50%", type="csv")
file_category_trend = st.sidebar.file_uploader("5️⃣ Category Trend Report (<10% & >50%)", type="csv")

# Color logic for bar graphs
def get_color_below(val, avg):
    return 'red' if val > avg + 5 else 'orange' if avg - 5 <= val <= avg + 5 else 'green'

def get_color_above(val, avg):
    return 'green' if val > avg + 5 else 'orange' if avg - 5 <= val <= avg + 5 else 'red'

def draw_zone_chart(df, label_col, is_below, title):
    df["Last week"] = df["Last week"].astype(str).str.replace("%", "").astype(float)
    df["This week"] = df["This week"].astype(str).str.replace("%", "").astype(float)

    labels = df[label_col].tolist()
    last = df["Last week"].tolist()
    this = df["This week"].tolist()
    avg = np.mean(this)
    x = np.arange(len(labels))
    width = 0.35

    zone_colors = [get_color_below(v, avg) if is_below else get_color_above(v, avg) for v in this]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width/2, last, width, color='white', edgecolor='black', label='Last Week')
    ax.bar(x + width/2, this, width, color=zone_colors, edgecolor='black', label='This Week')

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_ylabel("Batch %")
    ax.set_title(f"{title} (Avg: {avg:.2f}%)")

    legend_items = [
        Patch(facecolor='green', edgecolor='black', label='🟩 Healthy'),
        Patch(facecolor='orange', edgecolor='black', label='🟧 Watch Zone'),
        Patch(facecolor='red', edgecolor='black', label='🟥 Risk'),
        Patch(facecolor='white', edgecolor='black', label='⬜ Last Week'),
        Patch(facecolor='black', edgecolor='black', label='⬛ This Week'),
    ]
    ax.legend(handles=legend_items, loc='upper right', bbox_to_anchor=(1, 1))
    st.pyplot(fig)

if file_v_below:
    st.subheader("1️⃣ Vertical-wise BH < 10% (Risk)")
    df = pd.read_csv(file_v_below)
    df.columns = df.columns.str.strip()
    draw_zone_chart(df, label_col="Vertical", is_below=True, title="Vertical-wise BH < 10%")

if file_v_above:
    st.subheader("2️⃣ Vertical-wise BH > 50% (Healthy)")
    df = pd.read_csv(file_v_above)
    df.columns = df.columns.str.strip()
    draw_zone_chart(df, label_col="Vertical", is_below=False, title="Vertical-wise BH > 50%")

if file_c_below:
    st.subheader("3️⃣ Category-wise BH < 10% (Risk)")
    df = pd.read_csv(file_c_below)
    df.columns = df.columns.str.strip()
    draw_zone_chart(df, label_col="Category", is_below=True, title="Category-wise BH < 10%")

if file_c_above:
    st.subheader("4️⃣ Category-wise BH > 50% (Healthy)")
    df = pd.read_csv(file_c_above)
    df.columns = df.columns.str.strip()
    draw_zone_chart(df, label_col="Category", is_below=False, title="Category-wise BH > 50%")

# Zone tracking logic
def classify_zone_last(bh_below, bh_above):
    if bh_below <= 10 and bh_above > 25:
        return "✅ Healthy"
    elif bh_below <= 10 and bh_above <= 25:
        return "🟡 Watch"
    elif bh_below > 20 or bh_above < 10:
        return "🔴 At Risk"
    else:
        return "🟡 Watch"

def get_change(last, this):
    if last == this:
        return "– No Change"
    elif last == "🔴 At Risk" and this in ["🟡 Watch", "✅ Healthy"]:
        return "📈 Improved"
    elif last == "🟡 Watch" and this == "✅ Healthy":
        return "📈 Improved"
    elif last == "✅ Healthy" and this in ["🟡 Watch", "🔴 At Risk"]:
        return "📉 Declined"
    else:
        return "📉 Declined"

if file_category_trend:
    st.subheader("5️⃣ Category-wise Zone Tracking (Last Week vs This Week)")
    df_trend = pd.read_csv(file_category_trend)
    df_trend.columns = df_trend.columns.str.strip()

    for col in df_trend.columns[1:]:
        df_trend[col] = df_trend[col].astype(str).str.replace("%", "").astype(float)

    df_trend["Last Zone"] = df_trend.apply(lambda row: classify_zone_last(row["BH <10% Last"], row["BH >50% Last"]), axis=1)
    df_trend["This Zone"] = df_trend.apply(lambda row: classify_zone_last(row["BH <10% This"], row["BH >50% This"]), axis=1)
    df_trend["Zone Change"] = df_trend.apply(lambda row: get_change(row["Last Zone"], row["This Zone"]), axis=1)

    st.dataframe(df_trend[["Category", "BH <10% Last", "BH <10% This", "BH >50% Last", "BH >50% This", "Last Zone", "This Zone", "Zone Change"]].style
        .applymap(lambda v: "background-color:#f8d7da;" if v == "🔴 At Risk" else
                            "background-color:#fff3cd;" if v == "🟡 Watch" else
                            "background-color:#d4edda;" if v == "✅ Healthy" else "",
                  subset=["This Zone", "Last Zone"])
        .applymap(lambda v: "color:green;" if v == "📈 Improved" else
                            "color:red;" if v == "📉 Declined" else "",
                  subset=["Zone Change"])
    )

    st.markdown("### 🧠 Updated Insights with Zone Movement")
    for _, row in df_trend.iterrows():
        cat = row['Category']
        last = row['Last Zone']
        now = row['This Zone']
        change = row['Zone Change']
        low_last = row['BH <10% Last']
        low_now = row['BH <10% This']
        high_last = row['BH >50% Last']
        high_now = row['BH >50% This']

        st.markdown(f"#### {cat} ({last} → {now} | {change})")
        st.write(f"BH <10% changed: {low_last:.2f}% → {low_now:.2f}%")
        st.write(f"BH >50% changed: {high_last:.2f}% → {high_now:.2f}%")
        if change == "📈 Improved":
            st.success("Improved zone status — keep up the momentum.")
        elif change == "📉 Declined":
            st.error("Zone declined — investigate causes and take action.")
        else:
            st.info("Zone unchanged — maintain current strategy.")
        st.markdown("---")
