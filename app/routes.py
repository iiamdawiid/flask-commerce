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


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()

            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                flash("Login successful", "success")
                return redirect(url_for("index"))
            else:
                flash("Invalid email or password. Please try again.", "danger")
                return redirect(url_for("login"))
            
        else:
            flash("Invalid form. Please try again.", "danger")
            return redirect(url_for("login"))
    else:
        return render_template("login.html", form=form)
    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "danger")
    return redirect(url_for("login"))


@app.route("/my_cart", methods=['GET', 'POST'])
@login_required
def my_cart():
    url = "https://fakestoreapi.com/products"
    response = r.get(url)
    if response.ok:
        products = response.json()
    cart_items = CartItems.query.filter_by(user_id=current_user.id).all()

    return render_template("my_cart.html", cart_items=cart_items, products=products)


@app.route("/add_to_cart", methods=['POST'])
def add_to_cart():
    if current_user.is_authenticated:
        if request.method == 'POST':
            # product_id = request.form.get('product_id')
            product_image = request.form.get('product_image')
            product_title = request.form.get('product_title')
            product_price = request.form.get('product_price')
            product_category = request.form.get('product_category')

            cart_item = CartItems(item_image=product_image, item_name=product_title, category=product_category, price=product_price, user_id=current_user.id)

            db.session.add(cart_item)
            db.session.commit()
            flash(f'{product_title} was added to cart.', 'success')

            return redirect(url_for('index'))
    else:
        flash('Login or create an account to add to cart.', 'warning')
        return redirect(url_for('login'))

    return redirect(url_for('index'))


@app.route("/remove_from_cart", methods=['POST'])
@login_required
def remove_from_cart():
    if request.method == 'POST':
        item_id = request.form.get('item_id')

        item = CartItems.query.get(item_id)
        if item and item.user_id == current_user.id:
            db.session.delete(item)
            db.session.commit()
            flash(f'{item.item_name} was removed from your cart.', 'danger')
        else:
            flash('Item not found.', 'success')

    return redirect(url_for('my_cart'))