import pandas as pd
import plotly.graph_objects as go
import os

# Create output directory
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read the Excel file
input_file = os.path.join(output_dir, "Douban_Top_250_Movies_Split_Year_Genre.xlsx")
df = pd.read_excel(input_file)

# Group by rating and count the number of movies for each rating
rating_counts = df["Score"].value_counts().reset_index()
rating_counts.columns = ["Score", "Count"]

# Create a pie chart
fig = go.Figure(
    data=[go.Pie(labels=rating_counts["Score"], values=rating_counts["Count"], hole=0.3)]
)
fig.update_layout(
    title="Douban Top 250 Movies Score Distribution",
    template="plotly_white"
)

# Set hover text to show the score and corresponding movie count
fig.update_traces(hovertemplate="Score: %{label}<br>Count: %{value}")

# Save and display the chart
output_file = os.path.join(output_dir, "Douban_Movie_Score_Distribution.html")
fig.write_html(output_file)
print(f"Chart successfully saved as: {output_file}")
fig.show()
