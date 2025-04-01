from abc import ABC, abstractmethod
import pandas as pd
import praw
from datetime import datetime, timedelta
from .models import Sentiment_table


class DataCollector(ABC):
    def __init__(self, product, limit=None, last_updated=None):
        self.keyword = product.product_name
        self.product_id = product.id
        self.last_updated = self.get_last_updated()
        self.time_filter = self.set_time_period()
        self.limit = self.set_limit()

        print(f"Keyword: {self.keyword}")
        print(f"Last Updated: {self.last_updated}")
        print(f"Time Filter: {self.time_filter}")
        print(f"Limit: {self.limit}")
       

    @abstractmethod
    @abstractmethod
    def collect_data(self):
        pass
    
    @abstractmethod
    def set_time_period(self):
        pass

    @abstractmethod
    def get_last_updated(self):
        pass
    
    @abstractmethod
    def set_limit(self):
        pass


class RedditDataCollector(DataCollector):
    def __init__(self, keyword, limit):
        super().__init__(keyword, limit)
        self.reddit = self.create_reddit_instance()

    def create_reddit_instance(self):
        reddit = praw.Reddit(
            username="fyp24075",
            password="xyZtor-puzgu2-jimfif",
            client_id="FHEWKhsWocLDbEZUvGOTdw",
            client_secret="211TdovfNPAnQdGfchGeW0waKfOjbg",
            user_agent="fyp24075"
        )
        return reddit

    def collect_data(self):
        posts = []
        for submission in self.reddit.subreddit("all").search(self.keyword, limit=self.limit, time_filter=self.time_filter):
            posts.append({
            "id": submission.id,
            "title": submission.title,
            "body": submission.selftext,
            "num_comments": submission.num_comments,
            "url": submission.url,
            "date": pd.to_datetime(submission.created_utc, unit='s').date()
            })

        return posts
    
    def get_last_updated(self):
        sentiment = Sentiment_table.query.filter_by(product_id=self.product_id).order_by(Sentiment_table.post_date.desc()).first()
        return sentiment.create_date if sentiment else None
    
    def set_time_period(self):
        if self.last_updated:
            self.last_updated = pd.to_datetime(self.last_updated)
            now = pd.to_datetime(datetime.now())

            delta = now - self.last_updated
            if delta <= timedelta(days=1):
                return "day" 
            elif delta <= timedelta(days=7):
                return "week" 
            elif delta <= timedelta(days=30):
                return "month" 
            elif self.last_updated.year == now.year:
                return "year" 
            else:
                return "all" 
        else:
            return "all" 
        
    def set_limit(self):
        if self.time_filter == "day":
            return 3
        elif self.time_filter == "week":
            return 10
        elif self.time_filter == "month":
            return 30
        else:
            return 100
        
   