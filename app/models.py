from flask_sqlalchemy import SQLAlchemy
import copy
import random
from collections import deque

db = SQLAlchemy()


draw_subscription = db.Table(
    "draw_subscription",
    db.Column("draw_id", db.Integer, db.ForeignKey("draw.id"), primary_key=True),
    db.Column(
        "participant_id", db.Integer, db.ForeignKey("participant.id"), primary_key=True
    ),
)


class Draw(db.Model):
    """..."""

    __tablename__ = "draw"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    in_process = db.Column(db.Boolean, nullable=True, default=False)
    responsible_number = db.Column(db.String(120), unique=False, nullable=False)

    participants = db.relationship(
        "Participant", secondary=draw_subscription, backref="draws",
    )

    created_at = db.Column(
        db.DateTime, default=db.func.current_timestamp(), nullable=False
    )

    def __init__(self, in_process, responsible_number, participants=[], result={}):
        self.in_process = in_process
        self.responsible_number = responsible_number
        self.participants = participants
        self.result = {}

    def __repr__(self):
        return f"Draw: code={self.id}, responsible={self.responsible_number} created={self.created_at}"

    @staticmethod
    def create(responsible_number):
        draw = Draw(in_process=True, responsible_number=responsible_number)
        return draw

    def run(self):
        participants = copy.copy(self.participants)
        random.shuffle(self.participants)

        partners = deque(participants)
        partners.rotate()
        result = list(zip(participants, partners))
        return result


class Participant(db.Model):
    """Participant"""

    __tablename__ = "participant"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    number = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"Participant: name={self.name}, number={self.number}"

    @staticmethod
    def find_or_create(name, number):
        participant = Participant.query.filter_by(number=number).first()
        if not participant:
            participant = Participant(name=name, number=number)
        return participant
