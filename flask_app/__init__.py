# __init__.py
from flask import Flask, session
app = Flask(__name__)
app.secret_key = "password"
