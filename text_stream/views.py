from flask import request, render_template, session

from .app import app, db, socketio
from .models import Message
from .twilio_service import TwilioService


def _is_admin():
    return 'admin_username' in session


def require_admin(f):
    def require_admin_(*args, **kwargs):
        if _is_admin():
            return f(*args, **kwargs)
        return redirect('/')
    return require_admin_

def emit(message):
    socketio.emit("message", {"id": message.id, "content": message.content}, broadcast=True)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rainbow")
def rainbow():
    return render_template("rainbow.html")

@app.route("/admin", methods=["POST", "GET"])
def admin():
    username = request.form.get('username')
    if username and username in app.config["ADMINS"] and request.form.get('password') == app.config["ADMINS"][username]:
        session['admin_username'] = username

    if _is_admin():
        return render_template("admin.html")
    return render_template("authenticate.html")

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

@require_admin
@socketio.on("submit_message")
def submit_message(data):
    print(f"Creating message from {data}")
    db.session.add(Message(content=data.get("content")))
    db.session.commit()

@socketio.on("resend_all")
def resend_all():
    for m in Message.approved():
        emit(m)

@require_admin
@socketio.on("request_approvals")
def request_approvals():
    socketio.emit("approvals", Message.serialize(Message.pending_approval()))

@require_admin
@socketio.on("approve")
def approve_message(data):
    message = Message.query.get(data.get("message_id"))
    if message:
        message.approve()
        emit(message)
    else:
        print(f"no such message: {data}")

@require_admin
@socketio.on("reject")
def reject_message(data):
    message = Message.query.get(data.get("message_id"))
    if message:
        message.reject()
    else:
        print(f"no such message: {data}")


views_loaded = True
