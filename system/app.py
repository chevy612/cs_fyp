from flask import Flask, request, jsonify, render_template
import praw
import nltk
import pandas as pd
import tensorflow as tf
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from transformers import RobertaTokenizer, TFRobertaForSequenceClassification

app = Flask(__name__)

# NLTK setup
nltk.download('punkt')
nltk.download('stopwords')

# Load RoBERTa model
roberta_tokenizer = RobertaTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
roberta_model = TFRobertaForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

# Reddit API setup
reddit = praw.Reddit(
    username="fyp24075",
    password="xyZtor-puzgu2-jimfif",
    client_id="FHEWKhsWocLDbEZUvGOTdw",
    client_secret="211TdovfNPAnQdGfchGeW0waKfOjbg",
    user_agent="fyp24075"
)

# Functions
def collect_reddit_data(keyword, limit=100):
    posts = []
    for submission in reddit.subreddit("all").search(keyword, limit=limit):
        posts.append({
            "title": submission.title,
            "body": submission.selftext,
            "date": pd.to_datetime(submission.created_utc, unit='s').date()
        })
    return pd.DataFrame(posts)

def clean_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    cleaned_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    return ' '.join(cleaned_tokens)

def classify_sentiment(score):
    if score < -0.15:
        return 'Negative'
    elif score > 0.15:
        return 'Positive'
    else:
        return 'Neutral'

def analyze_sentiment_roberta(df, model):
    df['combined_text'] = df['title'] + " " + df['body']
    df['cleaned_data'] = df['combined_text'].apply(clean_text)
    
    sentiment_scores = []
    sentiments = []
    
    for cleaned_data in df['cleaned_data']:
        if cleaned_data.strip():
            inputs = roberta_tokenizer(cleaned_data, return_tensors="tf", max_length=512, truncation=True, padding=True)
            outputs = model(inputs)
            probabilities = tf.nn.softmax(outputs.logits, axis=1).numpy()[0]
            score = sum(prob * (i - 1) for i, prob in enumerate(probabilities))  # -1 to 1
            sentiment_scores.append(score)
            sentiments.append(classify_sentiment(score))
        else:
            sentiment_scores.append(None)
            sentiments.append(None)
    
    df['sentiment_score'] = sentiment_scores
    df['predicted_sentiment'] = sentiments
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    keyword = request.json['keyword']
    limit = 100
    
    df = collect_reddit_data(keyword, limit)
    df = analyze_sentiment_roberta(df, roberta_model)
    
    sentiment_counts = df['predicted_sentiment'].value_counts(normalize=True) * 100
    percentages = {
        'positive': round(sentiment_counts.get('Positive', 0), 1),
        'neutral': round(sentiment_counts.get('Neutral', 0), 1),
        'negative': round(sentiment_counts.get('Negative', 0), 1)
    }
    
    overall_score = round(df['sentiment_score'].mean() or 0, 1)
    overall_classified = classify_sentiment(overall_score)
    
    time_series = df.groupby('date')['sentiment_score'].mean().reset_index()
    time_series_data = {
        'dates': time_series['date'].astype(str).tolist(),
        'scores': [round(score, 1) for score in time_series['sentiment_score'].tolist()]
    }
    
    return jsonify({
        'percentages': percentages,
        'overall_score': overall_score,
        'overall_classified': overall_classified,
        'time_series': time_series_data
    })

if __name__ == '__main__':
    app.run(debug=True)