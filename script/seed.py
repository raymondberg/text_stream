from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.absolute()))
print(sys.path)

from app import db, Message

messages = {
    "approved": [
        "I'm allowed to take up space.",
        "My past is not a reflection of my future.",
        "I am smart enough to make my own decisions.",
        "I'm in control of how I react to others.",
        "I choose the calm of peace over the churn of hatred.",
        "I'm courageous and stand up for myself",
        "I will succeed today.",
        "I deserve to have joy in my life.",
    ],
    "rejected": [
        "you suck",
        "this is the worst",
        "get dumber",
    ],
}

for m in messages["approved"]:
    db.session.add(Message(content=m))

for m in messages["rejected"]:
    db.session.add(Message(content=m))

db.session.commit()
