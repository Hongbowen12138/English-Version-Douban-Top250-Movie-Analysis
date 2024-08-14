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

# Group by year and count the number of movies for each year
year_counts = df["Year"].value_counts().reset_index()
year_counts.columns = ["Year", "Count"]
year_counts = year_counts.sort_values(by="Year")

# Create a bar chart
fig = go.Figure(data=[go.Bar(x=year_counts["Year"], y=year_counts["Count"], marker_color='skyblue')])

# Set chart style and title
fig.update_layout(
    title="Douban Top 250 Movies: Year vs. Movie Count Bar Chart",
    xaxis_title="Year",
    yaxis_title="Movie Count",
    xaxis=dict(tickmode='linear'),
    template="plotly_white"
)

# Set hover text to show year and corresponding movie count
fig.update_traces(hovertemplate="Year: %{x}<br>Count: %{y}")

# Save and display the interactive bar chart
output_file = os.path.join(output_dir, "Douban_Movie_Count_Bar_Chart.html")
fig.write_html(output_file)
print(f"Chart successfully saved as: {output_file}")
fig.show()
