import requests
from lxml import etree
import pandas as pd
import re
import time
import random
import os

# Define request headers
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
    )
}

# Helper function: Get the first element of a list and strip surrounding whitespace
def get_first_text(text_list: list[str]) -> str:
    try:
        return text_list[0].strip()
    except IndexError:
        return ""

# Create output directory
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize data storage structure
COLUMNS = ["Index", "Title", "Link", "Score", "Year and Genre", "Actors"]
df = pd.DataFrame(columns=COLUMNS)

# Generate list of Douban Top 250 pagination URLs
START_OFFSETS = range(0, 250, 25)
URLS = [
    "https://movie.douban.com/top250?start={}&filter=".format(offset)
    for offset in START_OFFSETS
]

# Iterate over each pagination URL to fetch and parse movie information
for index, url in enumerate(URLS, start=1):
    try:
        print(f"Fetching URL: {url}")
        # Send network request
        response = requests.get(url=url, headers=HEADERS)
        response.raise_for_status()

        # Parse the HTML response into an ElementTree object
        html = etree.HTML(response.text)
        movie_lis = html.xpath('//*[@id="content"]/div/div[1]/ol/li')

        # Iterate over each movie li element, extract and process movie information
        for li in movie_lis:
            title = get_first_text(li.xpath("./div/div[2]/div[1]/a/span[1]/text()"))
            link = get_first_text(li.xpath("./div/div[2]/div[1]/a/@href"))
            score = get_first_text(li.xpath("./div/div[2]/div[2]/div/span[2]/text()"))
            yearandtype = get_first_text(li.xpath("./div/div[2]/div[2]/p[1]/text()[2]"))
            actor = get_first_text(li.xpath("./div/div[2]/div[2]/p[1]/text()"))

            print(f"Fetched movie: {title}, Score: {score}, Year and Type: {yearandtype}, Actors: {actor}")
            df.loc[len(df.index)] = [index, title, link, score, yearandtype, actor]

        # Add a random delay
        time.sleep(random.uniform(1, 5))

    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Error parsing or processing data: {e}")

# Save the DataFrame to an Excel file
df.to_excel(os.path.join(output_dir, "Douban_Top_250_Movies.xlsx"), sheet_name="Douban_Top_250_Movies", na_rep="")

# Read the generated Excel file
df = pd.read_excel(os.path.join(output_dir, "Douban_Top_250_Movies.xlsx"), sheet_name="Douban_Top_250_Movies")

# Use the split() function to split the year and genre
df["Year"] = df["Year and Genre"].apply(lambda x: re.sub(r"\D", "", x.split("/")[0]).lstrip())
df["Genre"] = df["Year and Genre"].apply(lambda x: " ".join(x.split("/")[1:]).replace("/", ""))

# Drop the old "Year and Genre" column
df.drop("Year and Genre", axis=1, inplace=True)

# Save the updated DataFrame to a new Excel file
df.to_excel(os.path.join(output_dir, "Douban_Top_250_Movies_Split_Year_Genre.xlsx"), sheet_name="Douban_Top_250_Movies", index=False)

print("Year and Genre have been split into separate columns, cleaned, and saved to a new file: output/Douban_Top_250_Movies_Split_Year_Genre.xlsx")
print("Excel file has been generated!")
