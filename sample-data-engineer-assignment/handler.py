import os
import requests
import pandas as pd

# Setup API vars
nyt_api_key = os.environ["NYT_API_KEY"]
nyt_api_endpoint = os.environ["NYT_API_ENDPOINT"]


def run(event, context):
    begin_date = 20230401
    end_date = 20230430

    # Set lookup file name
    lookup_file_name = "april_2023_nyt_articles.csv"

    try:
        status_r = requests.get(f"{nyt_api_endpoint}articlesearch.json?&begin_date={begin_date}&end_date={end_date}&sort=newest&api-key={nyt_api_key}")
    except Exception as e:
        print("Failed to make inital lookup request to Piano: " + str(e))
        return False
    status_response = status_r.json()

    article_collection = status_response["response"]["docs"]

    article_data = []

    for article in article_collection:
        formatted_article = {
            "_id": article["_id"],
            "pub_date": article["pub_date"],
            "headline": article["headline"]["main"],
            "section_name": article["section_name"],
            "word_count": article["word_count"],
            "snippet": article["snippet"]
        }
        article_data.append(formatted_article)

    # Create the dataframe
    tmp_file_path = f"{lookup_file_name}"

    data = pd.DataFrame(article_data)

    # Clean data
    data['snippet'] = data['snippet'].str[:50]
    data.to_csv(tmp_file_path, index=False)

    return "NYT article export complete"
