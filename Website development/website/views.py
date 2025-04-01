from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Search, Product, Sentiment_table
from .analyst import Analyst
from .presenter import Presenter  # Import the Presenter class
from datetime import datetime as dt, timedelta
import json

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def welcome():
    return render_template("welcome.html")

@views.route("/home", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_product = request.form.get("product")

        if not search_product:
            flash("Product name cannot be empty!", category="error")
            return redirect(url_for("views.search"))
        
        new_search = Search(search_product=search_product, user_id=current_user.id if current_user.is_authenticated else None)
        product_name = "".join(search_product.lower().split())  # the product name is the search product without spaces

        product = Product.query.filter_by(product_name=product_name).first()
        if not product:
            new_product = Product(product_name=product_name)
            db.session.add(new_product)
            db.session.commit()  # Commit to get the new_product.id
            new_search.product_id = new_product.id
            product = new_product  # Update the product variable to reference the newly created product
        else:
            new_search.product_id = product.id

        db.session.add(new_search)
        db.session.commit()

        # Instantiate and use the Analyst class to load the RoBERTa model and analyze sentiment
        analyst = Analyst(product, source='reddit')
        analyst.analyze_sentiment()

        flash("Searching the product", category="success")

        return redirect(url_for("views.report", search_product=search_product))
    
    return render_template("search.html", user=current_user if current_user.is_authenticated else None)

@views.route("/report", methods=["GET"])
def report():
    search_product = request.args.get("search_product")
    search = Search.query.filter_by(user_id=current_user.id if current_user.is_authenticated else None, search_product=search_product).order_by(Search.id.desc()).first()

    bar_data = None
    time_series_data = None
    percentages = None

    if search:
        product_id = search.product_id
        #three_months_ago = dt.now() - timedelta(days=90)
        print(f"Product ID: {product_id}")

        sentiments = Sentiment_table.query.filter(
            Sentiment_table.product_id == product_id,
        ).all()

        if sentiments:
            presenter = Presenter(search, sentiments)
            bar_data = presenter.bar
            time_series_data = presenter.time_series
            top_words_data = presenter.frequent_terms
            quarter_data = presenter.sentiment_by_quarter

            total = sum(bar_data.values())
            percentages = {
                'positive': (bar_data['Positive'] / total) * 100,
                'neutral': (bar_data['Neutral'] / total) * 100,
                'negative': (bar_data['Negative'] / total) * 100
            }
        else:
            bar_data = None
            time_series_data = []
            percentages = {'positive': 0, 'neutral': 0, 'negative': 0}
            top_words_data = []
            flash("No sentiments found!", category="error")
            return redirect(url_for("views.search"))
        
        flash("Product found!", category="success")
    else:
        bar_data = []
        time_series_data = {'date': [], 'sentiment': [] }
        percentages = {'positive': 0, 'neutral': 0, 'negative': 0}
        top_words_data = []
        flash("No products found!", category="error")
        return redirect(url_for("views.search"))   

    return render_template("report.html", user=current_user if current_user.is_authenticated else None, 
                           product_name=search_product, 
                           bar_data=json.dumps(bar_data), 
                           time_series_data=json.dumps(time_series_data), 
                           percentages=json.dumps(percentages),
                           top_words_data=json.dumps(top_words_data),
                           quarterly_data=json.dumps(quarter_data))


