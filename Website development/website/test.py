# Ensure the directory containing analyst.py is in the Python path
import sys
sys.path.append('/c:/Users/Chevy/OneDrive - The University of Hong Kong - Connect/Developer/Website development/website')

from analyst import Analyst
from models import Sentiment_table, Product, db
from presenter import Presenter
from datetime import datetime as dt, timedelta

# Create a new product
product = Product(product_name="iPhone16")
db.session.add(product)
db.session.commit()

# Instantiate and use the Analyst class to load the RoBERTa model and analyze sentiment
analyst = Analyst(product, source='reddit')
analyst.analyze_sentiment()

# Query the database for the sentiment analysis results
sentiments = Sentiment_table.query.filter_by(product_id=product.id).all()
for sentiment in sentiments:
    print(sentiment.cleaned_data)
    print(sentiment.predicted_sentiment)
    print(sentiment.sentiment_score)
    print(sentiment.post_date)
    print()
# Ensure the directory containing presenter.py is in the Python path

presenter = Presenter(sentiments)
print(presenter.show_sentiment_bar())



