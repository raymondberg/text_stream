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
        "Thanks for everything that you did for me this week!",
        "You are truly a great friend; thank you for being a golden girl",
        "Wowie wow wow I can't think of anything more positive to say",
        "Do you think my brain is going to start melting?",
        "Really these can be any sentences at all, it's just seed data",
        "Oh, that's a good point. Thanks for being so helpful with ideas and such",
    ],
    "rejected": [
        "you suck",
        "this is the worst",
        "get dumber",
    ],
}

for m in messages["approved"]:
    db.session.add(Message(content=m))
    db.session.commit()

for m in messages["rejected"]:
    db.session.add(Message(content=m))
    db.session.commit()

