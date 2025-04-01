import pandas as pd
from collections import Counter
#from .models import Sentiment_table

from transformers import pipeline
from transformers import AutoTokenizer


class Presenter:
    def __init__(self, search, sentiments_list):
        self.search_product = search.search_product
        self.sentiments = sentiments_list
        self.length = len(sentiments_list)
        self.df = self.sentiments_to_dataframe()
        self.bar = self.sentiment_distribution_bar()
        self.time_series = self.time_series_data()
        self.sentiment_by_quarter = self.sentiment_by_quarter()
        self.frequent_terms = self.frequent_terms()
        #self.summary = self.generate_summary()

        print("number of sentiments:", self.length)
        print("Bar Data:", self.bar)
        #print("Time Series Data:", self.time_series)
        print("Frequent Terms:", self.frequent_terms)
        print("Sentiment by Quarter:", self.sentiment_by_quarter)
        #print("Summary:", self.summary)

    def sentiments_to_dataframe(self):
        data = [{'date': sentiment.post_date, 
                 'sentiment': sentiment.sentiment_prediction, 
                 'score': sentiment.sentiment_score, 
                 'source_id': sentiment.source_id,
                 'text': sentiment.sentiment_text} for sentiment in self.sentiments]
        df = pd.DataFrame(data)
        df = df.drop_duplicates(subset='source_id', keep='first')
        return df
    
    def sentiment_distribution_bar(self):
        sentiment_distribution = self.df['sentiment'].value_counts().to_dict()
        sentiment_distribution = {
            'Positive': sentiment_distribution.get('Positive', 0),
            'Neutral': sentiment_distribution.get('Neutral', 0),
            'Negative': sentiment_distribution.get('Negative', 0)
        }
        return sentiment_distribution
    
    def time_series_data(self):
        self.df['date'] = pd.to_datetime(self.df['date']).dt.strftime('%Y-%m-%d')
        grouped_sentiment = self.df.groupby('date')['score'].mean().reset_index()
        time_series = {
            'date': grouped_sentiment['date'].tolist(),
            'sentiment': grouped_sentiment['score'].tolist()
        }
        return time_series
    
    def frequent_terms(self):
        all_words = ' '.join(self.df['text']).split()
        word_counts = Counter(all_words)
        most_common_words = word_counts.most_common(5)
        most_common_words = [{'word': word, 'count': count} for word, count in most_common_words]
        return most_common_words

    def sentiment_by_quarter(self):
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['quarter'] = self.df['date'].dt.to_period('Q')
        
        # Group by quarter and sentiment, then unstack to get counts for each sentiment
        grouped_quarter = self.df.groupby('quarter')['sentiment'].value_counts().unstack(fill_value=0)
        
        # Convert the grouped data to a list of dictionaries
        sentiment_by_quarter = []
        for quarter, counts in grouped_quarter.iterrows():
            sentiment_by_quarter.append({
                'quarter': str(quarter),
                'Negative': int(counts.get('Negative', 0)),
                'Neutral':int(counts.get('Neutral', 0)),
                'Positive': int(counts.get('Positive', 0))
            })
        
        return sentiment_by_quarter

    def generate_summary(self):

        comments = self.df['text'].tolist()
        comments_combined = ' '.join(comments)

        summarizer = pipeline("summarization")  
        tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        tokenized_comments = tokenizer.tokenize(comments_combined)

        if len(tokenized_comments) > 512:
            comments_combined = tokenizer.convert_tokens_to_string(tokenized_comments[:512])

        summarized = summarizer(comments_combined, min_length=70, max_length=160)
        summarized = summarized[0]['summary_text']
        return summarized






