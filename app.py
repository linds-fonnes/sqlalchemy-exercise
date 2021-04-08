"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from sqlalchemy import update

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = 'SecretSecretSecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def home_page():
    """redirects to /users"""
    return redirect("/users")

@app.route("/users")  
def list_users():
    """List current users and show add user button"""
    users = User.query.all()
    return render_template("users.html", users=users)  

@app.route("/users/new")
def show_form():
    """Shows form to add a new user"""
    return render_template("user_form.html")

@app.route("/users/new", methods=["POST"])
def add_user():
    """Adds user information to db and to home page"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("show_user.html",user=user)

@app.route("/users/<int:user_id>/edit")
def show_edit(user_id):
    """Displays page to edit user info"""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)  

@app.route("/users/<int:user_id>/edit", methods=["POST"])  
def edit_user(user_id):
    """Edits user info"""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Deletes user from db and home page"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect("/users")


    

