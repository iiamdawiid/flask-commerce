from app import app, db, bcrypt
from flask import render_template, request, redirect, url_for, flash, session
from .forms import SignUpForm, LoginForm, EditProfileForm
import requests as r
from flask_bcrypt import Bcrypt
from .models import User, CartItems
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/")
def index():
    url = "https://fakestoreapi.com/products"
    response = r.get(url)
    if response.ok:
        products = response.json()
        
    return render_template("index.html", products=products)

@app.route("/sign-up", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate():
            first_name = form.first_name.data.title()
            last_name = form.last_name.data.title()
            email = form.email.data
            password = form.password.data

            user_exists = User.query.filter_by(email=email).first()

            if user_exists:
                flash("A user with that email already exists. Please use a different email.", "danger")
                return redirect(url_for("signup"))
            else:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()

                flash('Account created successfully!', 'success')
                return redirect(url_for('login'))
        
        else:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('signup'))
    
    return render_template('sign-up.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()

            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                flash("Login Successful", "success")
                return redirect(url_for("index"))
            else:
                flash("Invalid email or password. Please try again.", "danger")
                return redirect(url_for("login"))
            
        else:
            flash("Invalid form. Please try again.", "danger")
            return redirect(url_for("login"))
    else:
        return render_template("login.html", form=form)

