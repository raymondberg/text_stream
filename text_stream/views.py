from flask import render_template

from .app import app, db, socketio
from .models import Message


def emit(message):
    socketio.emit("message", {"id": message.id, "content": message.content}, broadcast=True)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/rainbow")
def rainbow():
    return render_template("rainbow.html")

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


views_loaded = True
