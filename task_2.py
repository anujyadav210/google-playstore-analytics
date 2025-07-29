# -*- coding: utf-8 -*-
"""task_2.ipynb


Original file is located at
    https://colab.research.google.com/drive/1bwwpabf8ReR_vOr1kAl58Efs7VVv4k2R

#task 2:Use a grouped bar chart to compare the average rating and total review count for the top 10 app categories by number of installs. Filter out any categories where the average rating is below 4.0 and size below 10 M and last update should be Jan month . this graph should work only between 3PM IST to 5 PM IST apart from that time we should not show this graph in dashboard itself.
"""

#importing the required libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import webbrowser
import os
from datetime import datetime
import pytz

playstore_df=pd.read_csv('/content/drive/MyDrive/Play Store Data.csv')
playstore_df

playstore_df.isnull().sum()

#data preprocessing
playstore_df = playstore_df.dropna(subset=['Rating'])
for column in playstore_df.columns :
    playstore_df[column].fillna(playstore_df[column].mode()[0],inplace=True)
playstore_df.drop_duplicates(inplace=True)
playstore_df=apps_df=playstore_df[playstore_df['Rating']<=5]

playstore_df.isnull().sum()

playstore_df.duplicated().sum()

playstore_df.dtypes

##Convert the Installs columns to numeric by removing commas and +
playstore_df['Installs']=playstore_df['Installs'].str.replace(',','').str.replace('+','').astype(int)

playstore_df.dtypes

#converting the size from kb to mb to maintain consistency
def convert_size(size):
    if 'M' in size:
        return float(size.replace('M',''))
    elif 'k' in size:
        return float(size.replace('k',''))/1024
    else:
        return np.nan
apps_df['Size']=apps_df['Size'].apply(convert_size)

playstore_df.dtypes

#converting the last updated column to datetime format
playstore_df['Last Updated']=pd.to_datetime(playstore_df['Last Updated'])

playstore_df.dtypes

#applying filter in last updated column only for january month
playstore_df=playstore_df[playstore_df['Last Updated'].dt.month==1]

#Filter out any categories where the average rating is below 4.0 and size below 10 M and last update should be Jan month .
playstore_df=playstore_df[playstore_df['Rating']>=4.0]

playstore_df

#Replace 'Varies with device' and other invalids with real NaN
playstore_df['Size'] = playstore_df['Size'].replace(['Varies with device', 'NaN', '', ' '], np.nan)

playstore_df.isnull().sum()

#replacing the "varies with device " size to a constant size of more than 10
playstore_df['Size']=playstore_df['Size'].fillna(11.0)

playstore_df

#applying filter for the size only greater than 10
playstore_df=playstore_df[playstore_df['Size']>=10.0]

playstore_df

playstore_df.dtypes

#converting the reviews column to integer type
playstore_df['Reviews']=playstore_df['Reviews'].astype(int)

playstore_df.dtypes

#grouping the data on the basis of category
grouped_df = playstore_df.groupby('Category').agg({
    'Rating': 'mean',
    'Reviews': 'sum',
    'Installs': 'sum'
}).reset_index()

grouped_df

grouped_df.dtypes

#sorting the top 10 data
Top_10 = grouped_df.sort_values('Installs', ascending=False).head(10)

Top_10

# Melt the DataFrame to long format
melted_df = Top_10.melt(
    id_vars='Category',
    value_vars=['Rating', 'Reviews'],
    var_name='Metric',
    value_name='Count'
)

melted_df

#saving the plot as html files
html_files_path = "./"
if not os.path.exists(html_files_path):
    os.makedirs(html_files_path)

plot_containers = ""

# Save each Plotly figure to an HTML file with IST time-based visibility
def save_plot_as_html(fig, filename, insight):
    global plot_containers
    filepath = os.path.join(html_files_path, filename + ".html")
    html_content = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

    html_with_time_control = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Dashboard - Time Controlled</title>
        <style>
            body {{
                background-color: #111;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 20px;
            }}
            .plot-container {{
                margin: 30px auto;
                background-color: #222;
                padding: 15px;
                border-radius: 10px;
                width: 90%;
            }}
            .insights {{
                margin-top: 10px;
                font-size: 16px;
                color: #ccc;
            }}
        </style>
        <script>
            function showPlotIfInTime() {{
                const now = new Date();
                const options = {{
                    timeZone: 'Asia/Kolkata',
                    hour: '2-digit',
                    hour12: false
                }};
                const istHour = parseInt(new Intl.DateTimeFormat('en-US', options).format(now));

                if (istHour >= 15 && istHour < 17) {{
                    document.getElementById('plot-div').style.display = 'block';
                    document.getElementById('msg-div').style.display = 'none';
                }} else {{
                    document.getElementById('plot-div').style.display = 'none';
                    document.getElementById('msg-div').style.display = 'block';
                }}
            }}
            window.onload = showPlotIfInTime;
        </script>
    </head>
    <body>
        <h1> App Insights Dashboard</h1>

        <div id="msg-div" style="display: none;">
            <p> This chart is only available between <strong>3 PM and 5 PM IST</strong>.</p>
        </div>

        <div id="plot-div" class="plot-container" style="display: none;">
            <div class="plot">{html_content}</div>
            <div class="insights">{insight}</div>
        </div>
    </body>
    </html>
    """

    # Save to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_with_time_control)

# Create the Plotly figure
fig = px.bar(
    melted_df,
    x='Category',
    y='Count',
    color='Metric',
    labels={'Count': 'Value', 'Category': 'App Category'},
    title='Average Rating and Total Review Count for Top 10 Categories by Installs',
    color_discrete_map={'Rating': 'blue', 'Reviews': 'red'},
    width=1200,
    height=500,
    barmode='group'
)

fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size': 16},
    xaxis=dict(title_font={'size': 12}),
    yaxis=dict(title_font={'size': 12}),
    margin=dict(l=10, r=10, t=30, b=10)
)



# Save with time-restricted visibility
save_plot_as_html(
    fig=fig,
    filename="reviews_and_rating_count",
    insight='This shows count and average rating of top 10 app categories by installs.'
)
fig.show()