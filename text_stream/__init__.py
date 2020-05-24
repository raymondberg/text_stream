import datetime
import os

from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
socketio = SocketIO(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if 'SQLALCHEMY_DATABASE_URI' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../build/db.sqlite'

db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(240), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    approved_at = db.Column(db.DateTime, default=None, nullable=True)
    rejected_at = db.Column(db.DateTime, default=None, nullable=True)

    @classmethod
    def serialize(cls, message_data):
        if isinstance(message_data, cls):
            return message_data.to_json()
        return [m.to_json() for m in message_data]

    @classmethod
    def pending_approval(cls):
        return cls.query.filter(cls.approved_at==None, cls.rejected_at == None)

    @classmethod
    def approved(cls):
        return cls.query.filter(cls.approved_at!=None, cls.rejected_at == None)

    def approve(self):
        self.approved_at = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def reject(self):
        self.rejected_at = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Message {self.id}, approved={self.approved_at},rejected={self.rejected_at}>"

    def to_json(self):
        return {"id": self.id, "content": self.content}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/rainbow")
def rainbow():
    return render_template("rainbow.html")

def emit(message):
    socketio.emit("message", {"id": message.id, "content": message.content}, broadcast=True)

@app.route("/admin")
def admin():
    return render_template("admin.html")

@socketio.on("submit_message")
def submit_message(data):
    print(f"Creating message from {data}")
    db.session.add(Message(content=data.get("content")))
    db.session.commit()

@socketio.on("resend_all")
def resend_all():
    for m in Message.approved():
        emit(m)

@socketio.on("request_approvals")
def request_approvals():
    socketio.emit("approvals", Message.serialize(Message.pending_approval()))

@socketio.on("approve")
def approve_message(data):
    message = Message.query.get(data.get("message_id"))
    if message:
        message.approve()
        emit(message)
    else:
        print(f"no such message: {data}")

@socketio.on("reject")
def reject_message(data):
    message = Message.query.get(data.get("message_id"))
    if message:
        message.reject()
    else:
        print(f"no such message: {data}")
