### Project Overview

The main goal of this project is to scrape data from the Douban movie website's Top 250 list and perform data analysis and visualization on the extracted data. The project is divided into the following sections:

1. **Data Scraping (`douban_movie_crawler.py`)**
   - **Principle**: Using the `requests` library to send HTTP requests and retrieve the webpage content of Douban's Top 250 movies. The `lxml` library is then used to parse the HTML and extract relevant information such as movie titles, links, ratings, year and genre, and cast members.
   - **Anti-Scraping Techniques**:
     - **Simulating User Requests**: By setting the `User-Agent` header to mimic browser requests, the script avoids being blocked by the website.
     - **Random Delays**: Introducing random delays between requests to simulate human browsing behavior and avoid detection by the website due to abnormal request frequency.
     - **Exception Handling**: Using `try-except` blocks to catch any exceptions during the request and parsing process, ensuring that the script doesn't crash and logs any errors encountered.

2. **Data Processing and Cleaning**
   - **Principle**: Reading the scraped data and splitting the year and genre information into separate columns for a more structured dataset.
   - **Operations**:
     - Read the Excel file and split the year and genre columns.
     - Remove the original "Year and Genre" column and retain the cleaned data.

3. **Data Visualization**
   - **Scatter Plot (`douban_visual_scatter_plot.py`)**:
     - **Principle**: Using the `plotly.express` library to create an interactive scatter plot that shows the relationship between movie ratings and years, with movie titles as labels.
     - **Steps**: Read the processed data, add random jitter to simulate scatter plot variation, create the interactive scatter plot, and save it as an HTML file.
   - **Bar Chart (`visual_bar_chart.py`)**:
     - **Principle**: Using the `plotly.graph_objects` library to create a bar chart showing the distribution of movies across different years.
     - **Steps**: Read the processed data, group by year to count the number of movies, create the bar chart, and save it as an HTML file.
   - **Pie Chart (`visual_pie_chart.py`)**:
     - **Principle**: Using the `plotly.graph_objects` library to create a pie chart displaying the distribution of movies across different ratings.
     - **Steps**: Read the processed data, group by rating to count the number of movies, create the pie chart, and save it as an HTML file.

### Detailed Explanation of Anti-Scraping Techniques

1. **Simulating User Requests**:
   - By setting the `User-Agent` header to mimic browser requests, the script avoids being identified as a bot by the website. For example:
     ```python
     HEADERS = {
         "User-Agent": (
             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
         )
     }
     ```

2. **Random Delays**:
   - Introducing random delays between requests to simulate human browsing behavior, preventing the website from detecting abnormal request patterns. For example:
     ```python
     import time
     import random

     time.sleep(random.uniform(1, 5))
     ```

3. **Exception Handling**:
   - Using `try-except` blocks to catch any exceptions during the request and parsing process, ensuring that the script doesn't crash and logging any errors for further investigation. For example:
     ```python
     try:
         response = requests.get(url, headers=HEADERS)
         response.raise_for_status()
     except requests.RequestException as e:
         print(f"Request failed: {e}")
     ```

### Execution Command

To run the main script, execute the following command in your terminal:

```bash
python main.py
```

This will sequentially run each subscript, completing the entire process of data scraping, processing, and visualization. Each script will print output information to the console, making it easy to monitor the execution status and debug if necessary.