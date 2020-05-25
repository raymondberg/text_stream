from flask import request, render_template

from .app import app, db, socketio
from .models import Message
from .twilio_service import TwilioService


def emit(message):
    socketio.emit("message", {"id": message.id, "content": message.content}, broadcast=True)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rainbow")
def rainbow():
    return render_template("rainbow.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@TwilioService.is_valid_request
@app.route("/post/sms", methods=["POST"])
def sms_post():
    content = request.values.get('Body', None)

    print(content)
    if content:
        if TwilioService.is_too_long(content):
            return TwilioService.Responses.too_long()

        db.session.add(Message(content=content))
        db.session.commit()

        return TwilioService.Responses.success()

    return TwilioService.Responses.unknown()

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
