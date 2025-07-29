# -*- coding: utf-8 -*-
"""task3.ipynb


Original file is located at
    https://colab.research.google.com/drive/1lmdKd_nSa80qq8OubEp3AYQBkcQu7iFQ

#. Plot a bubble chart to analyze the relationship between app size (in MB) and average rating, with the bubble size representing the number of installs. Include a filter to show only apps with a rating higher than 3.5 and that belong to the Game, Beauty ,business , commics , commication , Dating , Entertainment , social and event categories. Reviews should be greater than 500 and the app name should not contain letter "S" and sentiment subjectivity should be more than 0.5 and highlight the Game Category chart in Pink color. We have to translate the Beauty category in Hindi and Business category in Tamil and Dating category in German while showing it on Graphs. Installs should be more than 50k as well as this graph should work only between 5 PM IST to 7 PM IST apart from that time we should not show this graph in dashboard itself.
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

#importing the dataset
playstore_df=pd.read_csv('/content/drive/MyDrive/Play Store Data.csv')
playstore_df.head()

reviews_df=pd.read_csv('/content/drive/MyDrive/User Reviews (1).csv')
reviews_df.head()

# Data Cleaning
playstore_df = playstore_df.dropna(subset=['Rating'])
for column in playstore_df.columns :
    playstore_df[column].fillna(playstore_df[column].mode()[0],inplace=True)
playstore_df.drop_duplicates(inplace=True)
playstore_df=playstore_df[playstore_df['Rating']<=5]
reviews_df.dropna(subset=['Translated_Review'],inplace=True)

#Convert the Installs columns to numeric by removing commas and +
playstore_df['Installs']=playstore_df['Installs'].str.replace(',','').str.replace('+','').astype(int)

playstore_df.dtypes

reviews_df.dtypes

playstore_df.isnull().sum()

reviews_df.isnull().sum()

reviews_df.duplicated().sum()

reviews_df.drop_duplicates(inplace=True)

reviews_df.duplicated().sum()

#merging both the datasets on the basis of same apps
merged_df=pd.merge(playstore_df,reviews_df,on='App',how='inner')

merged_df.head(5)

#checking for null values in merged dataset
merged_df.isnull().sum()

merged_df.duplicated().sum()

merged_df['Size'].unique()

#conversion of size in to MB
def convert_size(size):
    if 'M' in size:
        return float(size.replace('M',''))
    elif 'k' in size:
        return float(size.replace('k',''))/1024
    else:
        return np.nan
merged_df['Size']=merged_df['Size'].apply(convert_size)

merged_df['Size'].unique()

merged_df.dtypes

#conversion of reviews column datatype into integer
merged_df['Reviews']=merged_df['Reviews'].astype(int)

merged_df.dtypes

merged_df.isnull().sum()

merged_df.dropna(inplace=True)

#applying filters as per the task 3 first is filtering apps with rating greater than 3.5
merged_df=merged_df[merged_df['Rating']>3.5]

merged_df

#filtering apps  that belong to the Game, Beauty ,business , commics , commication , Dating , Entertainment , social and event categories
merged_df=merged_df[merged_df['Category'].isin(['GAME','BEAUTY','BUSINESS','COMICS','COMMUNICATION','DATING','ENTERTAINMENT','SOCIAL','EVENTS'])]

merged_df.head(5)

merged_df['Category'].unique()

#applying the third filter as per task 3 that is reviews should be greater than 5
merged_df=merged_df[merged_df['Reviews']>500]

merged_df['Reviews'].unique()

merged_df.head(5)

merged_df['Category'].unique()

#filtering out the apps which contains letter 's' in their strings
merged_df = merged_df[~merged_df['App'].str.contains("s", case=False, na=False)]

merged_df['Category'].unique()

merged_df

#applying another filter that is filtering apps with sentiment subjectivity more than 0.5
merged_df=merged_df[merged_df['Sentiment_Subjectivity']>0.5]

merged_df['Sentiment_Subjectivity'].unique()

merged_df['App'].unique()

#to translate the Beauty category in Hindi and Business category in Tamil and Dating category in German while showing it on Graphs.
merged_df['Category']=merged_df['Category'].replace({'BEAUTY':'सौंदर्य','BUSINESS':'வணிகம்','DATING':'Verabredung'})

merged_df

merged_df['Installs'].unique()

#filtering apps with installs more than 50000
merged_df=merged_df[merged_df['Installs']>50000]

merged_df['Installs'].unique()

#check for null if any left
merged_df.isnull().sum()

merged_df['Category'].unique()

#saving the plots as html document
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

                // Show chart only between 17:00 and 19:00 IST (5 PM to 7 PM)
                if (istHour >= 17 && istHour < 19) {{
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
        <h1> bubble chart Dashboard</h1>

        <div id="msg-div" style="display: none;">
            <p> This chart is only available between <strong>5 PM and 7 PM IST</strong>.</p>
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

#ploting the bubble chart
fig = px.scatter(
    merged_df,
    x='Size',
    y='Rating',
    size='Installs',
    color='Category',
    hover_name='App',
    size_max=200,
    title='App Size vs Rating with Bubble Size Representing Installs',
    labels={'Size': 'App Size (MB)', 'Rating': 'Average Rating'},
    color_discrete_map={'GAME': 'pink','SOCIAL':'green'}
)


# Dark theme styling
fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font_color='white',
    title_font={'size': 16},
    xaxis=dict(title='App Size (MB)', title_font={'size': 12}),
    yaxis=dict(title='Average Rating', title_font={'size': 12}),
    margin=dict(l=10, r=10, t=30, b=10)
)
# Save the plot
save_plot_as_html(
    fig=fig,
    filename="app_size vs rating_bubblechart",
    insight='this figure shows the rating of the app on the basis of the app.')
fig.show()
