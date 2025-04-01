# This part will be handling the product name input from the search() in views.py 
# and passing it to the data_pip.py file. 
# The data_pip.py file will then use the product name to scrape the data from the website 
# and return the data to the views.py file. 
# The views.py file will then display the data to the user.
# The data will also be stored in the database.

import praw
import pandas as pd
import datetime as datetime

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from .data_collector import RedditDataCollector
from .sentiment_analysis import analyze_sentiment_roberta, plot_sentiment_over_time

from .models import Sentiment_table, db
class Analyst:
    def __init__(self, product, source='reddit'):
        self.product = product
        self.product_name = self.format_product_name(product.product_name)
        self.source = source
        self.collector = self.create_collector(product)
        self.posts = self.collect_data()
        self.df = self.convert_to_df()
    
    def clean_text(self, text):
        tokens = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        cleaned_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
        return ' '.join(cleaned_tokens)

    def format_product_name(self, product_name):
        return product_name.lower().replace(" ", "")

    def create_collector(self, product):
        if self.source == 'reddit':
            return RedditDataCollector(product,limit=None)
        else:
            raise ValueError("Unsupported data source")

    def collect_data(self):
        return self.collector.collect_data()

    def convert_to_df(self):
        df = pd.DataFrame(self.posts)
        print(df[['title', 'body']])
        df['combined_text'] = df['title'] + " " + df.get('body', '')
        df['cleaned_data'] = df['combined_text'].apply(self.clean_text)
        
        return df

    def analyze_sentiment(self):
        if self.source == 'reddit':
            analyze_sentiment_roberta(self.df)
            #plot_sentiment_over_time(self.df)
            self.save_to_db()
        else:
            raise ValueError("Unsupported data source")

    def save_to_db(self):
        for _, row in self.df.iterrows():
            sentiment = Sentiment_table(
                product_name=self.product_name,
                post_date=row['date'],  
                sentiment_text=row['cleaned_data'],
                sentiment_score=row['sentiment_score'],
                sentiment_prediction=row['predicted_sentiment'],
                source=self.source,
                source_id=row['id'],  
                create_date= db.func.now(),
                product_id= self.product.id
            )
            db.session.add(sentiment)
        db.session.commit()



