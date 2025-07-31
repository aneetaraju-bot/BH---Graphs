import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Patch

# Sample data for BH < 10%
data_below_10 = {
    'Vertical': ['Commerce', 'Technical', 'Digital Marketing', 'Coding', 'Hospital Administration', 'Teaching'],
    'Last week': [6.49, 0.0, 14.71, 56.78, 6.67, 21.74],
    'This week': [6.25, 0.0, 18.52, 55.88, 0.0, 10.98]
}

# Sample data for BH > 50%
data_above_50 = {
    'Vertical': ['Commerce', 'Technical', 'Digital Marketing', 'Coding', 'Hospital Administration', 'Teaching'],
    'Last week': [18.18, 20.59, 0.0, 0.0, 13.33, 11.96],
    'This week': [17.5, 15.15, 0.0, 0.0, 15.38, 14.63]
}

df_below = pd.DataFrame(data_below_10)
df_above = pd.DataFrame(data_above_50)

# Define zone logic
def get_zone_color_below(last, current):
    diff = current - last
    if diff > 1:
        return 'red'     # Risk increasing
    elif diff < -1:
        return 'green'   # Healthy improving
    else:
        return 'orange'  # Watch zone

def get_zone_color_above(last, current):
    diff = current - last
    if diff > 1:
        return 'green'   # Healthy improving
    elif diff < -1:
        return 'red'     # Risk increasing (bad)
    else:
        return 'orange'  # Watch zone

# Plot function
def plot_dual_bar(df, title, is_below=True, filename="output.png"):
    categories = df["Vertical"].tolist()
    last_vals = df["Last week"].tolist()
    this_vals = df["This week"].tolist()
    
    x = np.arange(len(categories))
    width = 0.35

    # Color bar for "this week" based on logic
    colors_this_week = [
        get_zone_color_below(last_vals[i], this_vals[i]) if is_below else get_zone_color_above(last_vals[i], this_vals[i])
        for i in range(len(categories))
    ]

    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Bars
    ax.bar(x - width/2, last_vals, width, label='Last Week', color='gray', edgecolor='black')
    ax.bar(x + width/2, this_vals, width, label='This Week', color=colors_this_week, edgecolor='black')

    # Labels
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.set_ylabel("Percentage")
    ax.set_title(title)

    # Custom legend
    legend_elements = [
        Patch(facecolor='green', edgecolor='black', label='🟩 Healthy Zone'),
        Patch(facecolor='orange', edgecolor='black', label='🟧 Watch Zone'),
        Patch(facecolor='red', edgecolor='black', label='🟥 Risk Zone'),
        Patch(facecolor='gray', edgecolor='black', label='⬛ Last Week'),
        Patch(facecolor='white', edgecolor='black', label='⬜ This Week (Zone Color)')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

# Plot both charts
plot_dual_bar(df_below, "Vertical-wise BH < 10%", is_below=True, filename="bh_below_10_colored.png")
plot_dual_bar(df_above, "Vertical-wise BH > 50%", is_below=False, filename="bh_above_50_colored.png")
