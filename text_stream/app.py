import os

from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
socketio = SocketIO(app)


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if 'SQLALCHEMY_DATABASE_URI' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../build/db.sqlite'

app.config['SMS_NUMBER'] = os.environ.get('TWILIO_SMS_NUMBER', False)
if 'ADMINS' in os.environ:
    app.config['ADMINS'] = {
        entry.split("===")[0]: entry.split("===")[1] for entry in os.environ['ADMINS'].split(":::")
    }

db = SQLAlchemy(app)

