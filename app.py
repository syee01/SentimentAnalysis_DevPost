import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, redirect, url_for, request, render_template, session

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    reviews_folder = 'reviews'
    for file_name in os.listdir(reviews_folder):
        # Read the file contents
        filename = file_name
        return render_template('index.html', filename = filename)

@app.route('/', methods=['POST'])
def index_post():
    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Create client using endpoint and key
        credential = AzureKeyCredential(cog_key)
        cog_client = TextAnalyticsClient(endpoint=cog_endpoint, credential=credential)

        # Analyze each text file in the reviews folder
        reviews_folder = 'reviews'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            # Get language
            detectedLanguage = cog_client.detect_language(documents=[text])[0]
            language = '{}'.format(detectedLanguage.primary_language.name)

            # Get sentiment
            sentimentAnalysis = cog_client.analyze_sentiment(documents=[text])[0]
            sentiment = "{}".format(sentimentAnalysis.sentiment)
            if sentiment == 'neutral':
                sentiment = 'negative'
            print('\n'+sentiment)

            phrases = cog_client.extract_key_phrases(documents=[text])[0].key_phrases
            if len(phrases) > 0:
                print("\nKey Phrases:")
                for phrase in phrases:
                    print('\t{}'.format(phrase))
   
    except Exception as ex:
        print(ex)

    return render_template(
                'results.html',
                reviews = text,
                language = language,
                sentiment = sentiment,
                keyphrase = phrase
                )
        
 
    




