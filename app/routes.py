from app import app, db
from flask import render_template, request, redirect, url_for, flash, session
from .forms import PokemonForm, SignUpForm, LogInForm, EditProfileForm, CatchPokemonForm
import requests as r
from .models import User, CatchPokemon
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
def index():
    return render_template('index.html')