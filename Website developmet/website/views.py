from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Search
#from .analyst import fetch_reddit_data


views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def welcome():
    return render_template("welcome.html")

@views.route("/home", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1:
            flash("Note is too short!", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category="success")
    return render_template("home.html", user=current_user)

@views.route("/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        product_name = request.form.get("product")
        if not product_name:
            flash("Product name cannot be empty!", category="error")
            return redirect(url_for("views.search"))
        
        else:
            new_search = Search(product_name=product_name, user_id=current_user.id if current_user.is_authenticated else None)
            db.session.add(new_search)  
            db.session.commit()
            flash("Searching the product", category="success")

        return render_template("report.html", user=current_user if current_user.is_authenticated else None, product_name=product_name)    
    
    return render_template("search.html", user=current_user if current_user.is_authenticated else None)

@views.route("/report", methods=["GET"])
def report():
    search = Search.query.filter_by(user_id=current_user.id if current_user.is_authenticated else None).order_by(Search.id.desc()).first()
    flash("Product found!", category="success")
    product = search.product_name
    
    return render_template("report.html", user=current_user if current_user.is_authenticated else None, product_name=product)

