from flask_sqlalchemy import SQLAlchemy
import copy
import random
from collections import deque

db = SQLAlchemy()


class DrawSubscription(db.Model):
    __tablename__ = "draw_subscription"
    draw_id = db.Column(db.Integer, db.ForeignKey("draw.id"))
    participant_id = db.Column(
        db.Integer, db.ForeignKey("participant.id"), primary_key=True,
    )

    pair = db.Column(db.Integer, db.ForeignKey("participant.id"), nullable=True)

    draw = db.relationship(
        "Draw", back_populates="participants", foreign_keys=[draw_id]
    )
    participant = db.relationship(
        "Participant", back_populates="draws", foreign_keys=[participant_id]
    )


class Draw(db.Model):
    """..."""

    __tablename__ = "draw"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    in_process = db.Column(db.Boolean, nullable=True, default=False)
    responsible_number = db.Column(db.String(120), unique=False, nullable=False)

    participants = db.relationship(
        "DrawSubscription",
        back_populates="draw",
        primaryjoin="Draw.id==DrawSubscription.draw_id",
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
        db.session.add(draw)
        return draw

    def subscribe(self, participant):
        self.participants.append(DrawSubscription(participant=participant))

    def run(self):
        participants = copy.copy(self.participants)
        random.shuffle(participants)
        
        partners = deque(participants)
        partners.rotate()
        result = list(zip(participants, partners))
        for (subs1, subs2) in result:
            subs1.pair = subs2.participant
        return result


class Participant(db.Model):
    """Participant"""

    __tablename__ = "participant"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    number = db.Column(db.String(120), unique=True, nullable=False)

    draws = db.relationship(
        "DrawSubscription",
        back_populates="participant",
        primaryjoin="Participant.id==DrawSubscription.participant_id",
    )

    def get_draws(self):
        return [d.pair for d in self.draws]

    def __repr__(self):
        return f"Participant: name={self.name}, number={self.number}"

    @staticmethod
    def find_or_create(name, number):
        participant = Participant.query.filter_by(number=number).first()
        if not participant:
            participant = Participant(name=name, number=number)
            db.session.add(participant)
        return participant
