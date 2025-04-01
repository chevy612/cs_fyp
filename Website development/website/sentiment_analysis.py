import praw
import nltk
import pandas as pd
import tensorflow as tf
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from transformers import BertTokenizer, TFBertForSequenceClassification
from transformers import RobertaTokenizer, TFRobertaForSequenceClassification
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Initialize NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load pre-trained models
bert_tokenizer = BertTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
bert_model = TFBertForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

roberta_tokenizer = RobertaTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
roberta_model = TFRobertaForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

def classify_sentiment(score):
    if score < -0.1:
        return 'Negative'
    elif score > 0.1:
        return 'Positive'
    else:
        return 'Neutral'

def analyze_sentiment_bert(df):
    for index, row in df.iterrows():
        cleaned_data = row['cleaned_data']
        if cleaned_data.strip():
            inputs = bert_tokenizer(cleaned_data, return_tensors="tf", max_length=512, truncation=True, padding=True)
            outputs = bert_model(inputs)
            probabilities = tf.nn.softmax(outputs.logits, axis=1).numpy()[0]
            sentiment_score = sum(prob * (i - 2) for i, prob in enumerate(probabilities)) / 2
            sentiment_label = classify_sentiment(sentiment_score)
            df.at[index, 'sentiment_score'] = sentiment_score
            df.at[index, 'predicted_sentiment'] = sentiment_label
        else:
            df.at[index, 'predicted_sentiment'] = None
            df.at[index, 'sentiment_score'] = None

def analyze_sentiment_roberta(df):
    for index, row in df.iterrows():
        cleaned_data = row['cleaned_data']
        if cleaned_data.strip():
            inputs = roberta_tokenizer(cleaned_data, return_tensors="tf", max_length=512, truncation=True, padding=True)
            outputs = roberta_model(inputs)
            probabilities = tf.nn.softmax(outputs.logits, axis=1).numpy()[0]
            sentiment_score = sum(prob * (i - 1) for i, prob in enumerate(probabilities))
            sentiment_label = classify_sentiment(sentiment_score)
            df.at[index, 'sentiment_score'] = sentiment_score
            df.at[index, 'predicted_sentiment'] = sentiment_label
        else:
            df.at[index, 'predicted_sentiment'] = None
            df.at[index, 'sentiment_score'] = None

def evaluate_performance(true_labels, predicted_labels):
    accuracy = accuracy_score(true_labels, predicted_labels)
    precision = precision_score(true_labels, predicted_labels, average='weighted')
    recall = recall_score(true_labels, predicted_labels, average='weighted')
    f1 = f1_score(true_labels, predicted_labels, average='weighted')
    print(f"Model Accuracy: {accuracy:.4f}")
    print(f"Model Precision: {precision:.4f}")
    print(f"Model Recall: {recall:.4f}")
    print(f"Model F1 Score: {f1:.4f}")

def plot_sentiment_over_time(df):
    df['date_by_week'] = pd.to_datetime(df['date']).dt.to_period('W').apply(lambda r: r.start_time)
    sentiment_over_time = df.groupby('date_by_week')['sentiment_score'].mean().reset_index()
    plt.figure(figsize=(12, 6))
    plt.plot(sentiment_over_time['date_by_week'], sentiment_over_time['sentiment_score'], marker='o', linestyle='-')
    plt.title('Average Sentiment Score Over Time')
    plt.xlabel('Date')
    plt.ylabel('Average Sentiment Score')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()
