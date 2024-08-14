import pandas as pd
import numpy as np
import plotly.express as px
import webbrowser
import os

# Create output directory
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read Excel data
input_file = os.path.join(output_dir, "Douban_Top_250_Movies_Split_Year_Genre.xlsx")
print(f"Reading data from {input_file}")
df = pd.read_excel(input_file, sheet_name="Douban_Top_250_Movies")

# Select the first 150 rows and remove duplicates, keeping unique combinations of score and year
df_unique = df.head(150).drop_duplicates(subset=["Score", "Year"])

# Add random noise to simulate scatter plot jitter
jitter_amount = 4  # Adjust this value to control jitter intensity; the smaller the value, the less jitter
np.random.seed(42)  # Set a random seed for reproducibility
df_unique["Score"] = df_unique["Score"] + jitter_amount * np.random.normal(size=len(df_unique))
df_unique["Year"] = df_unique["Year"] + jitter_amount * np.random.normal(size=len(df_unique))

# Round the score to 1 decimal place, year to 0 decimal places
df_unique["Score"] = df_unique["Score"].round(1)
df_unique["Year"] = df_unique["Year"].astype(int)

print("Creating scatter plot")
# Create interactive scatter plot
fig = px.scatter(
    df_unique,
    x="Score",
    y="Year",
    hover_data=["Title", "Genre", "Actors"],
    text="Title",
    template="plotly_white",  # Use Plotly white background template
)

# Convert movie titles into clickable links
for i, (index, row) in enumerate(df_unique.iterrows()):
    fig.data[0].text[i] = f'<a href="{row["Link"]}" target="_blank">{row["Title"]}</a>'

# Customize plot layout
fig.update_layout(
    showlegend=False,
    title_text="Douban Movie Scores and Years Scatter Plot",
    title_font_size=20,
    xaxis_title="Score",
    yaxis_title="Year",
    xaxis=dict(range=[df["Score"].min() - 0.1, df["Score"].max() + 0.1], automargin=True, showgrid=True),
    yaxis=dict(range=[df["Year"].min() - 5, df["Year"].max() + 5], automargin=True, showgrid=True)
)

# Position text labels
fig.update_traces(textposition="top center")

# Save and open the plot
output_file = os.path.join(output_dir, "interactive_scatterplot_plotly_with_jitter.html")
fig.write_html(output_file)
print(f"Scatter plot saved to {output_file}")
webbrowser.open(output_file)
