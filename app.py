from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "asdfghjk"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'  # Use your own URI
db = SQLAlchemy(app)
