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

# Initialize PRAW with your credentials
class Analyst:
    def __init__(self,product_name):
        self.product_name = product_name
        self.reddit = self.create_reddit_instance()

        self.posts = self.fetch_reddit_data()
        self.df = self.convert_to_df()
    
    def clean_text(self, text):
        tokens = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        cleaned_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
        return ' '.join(cleaned_tokens)

    def create_reddit_instance(self):
        reddit = praw.Reddit(
            username="fyp24075",
            password="xyZtor-puzgu2-jimfif",
            client_id="FHEWKhsWocLDbEZUvGOTdw",
            client_secret="211TdovfNPAnQdGfchGeW0waKfOjbg",
            user_agent="fyp24075"
        )
        return reddit

    def fetch_reddit_data(self):
        posts = []
        reddit = self.create_reddit_instance()
        limit = 10
        for submission in reddit.subreddit("all").search(self.product_name, limit=limit):
            posts.append({
                "title": submission.title,
                "body": submission.selftext,
                "num_comments": submission.num_comments,
                "url": submission.url,
                "date": pd.to_datetime(submission.created_utc, unit='s').date()
            })
        return posts
    
    def convert_to_df(self):
        df = pd.DataFrame(self.posts)
        df['combined_text'] = df['title'] + " " + df['body']
        
        clean_data_list = []
        for each_post_text in df['combined_text']:
            clean_data_list.append(self.clean_text(each_post_text))

        df['clean_data'] = clean_data_list

        return df


    
        
          



analyst = Analyst("BTC")
df = analyst.convert_to_df()
print(df)

