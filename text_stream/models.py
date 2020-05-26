import csv
import datetime
import io

from .app import db

class Message(db.Model):
    SERIALIZED_HEADERS = ["id","content"]
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
    def as_csv(cls, dataset=None):
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=cls.SERIALIZED_HEADERS)
        for m in cls.serialize(dataset or cls.query.all()):
            writer.writerow(m)
        return output.getvalue()

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
        return {att: getattr(self, att) for att in self.SERIALIZED_HEADERS}


models_loaded = True
