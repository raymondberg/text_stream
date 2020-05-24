import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if 'SQLALCHEMY_DATABASE_URI' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(240), nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=False)
    approved_at = db.Column(db.DateTime, default=None, nullable=True)

    def __repr__(self):
        return '<Message {self.message}>'

@app.route("/")
def home():
    return render_template("index.html", messages=[Message(content="hi")])
