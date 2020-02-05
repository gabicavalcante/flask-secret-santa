from flask_sqlalchemy import SQLAlchemy
import copy
import random

db = SQLAlchemy()


draw_subscription = db.Table(
    "DrawSubscription",
    db.Column("draw_id", db.Integer, db.ForeignKey("draw.id"), primary_key=True),
    db.Column(
        "participant_id", db.Integer, db.ForeignKey("participant.id"), primary_key=True
    ),
)


class Draw(db.Model):
    """..."""

    __tablename__ = "draw"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=True)
    in_process = db.Column(db.Boolean, nullable=True, default=False)
    responsible_number = db.Column(db.String(120), unique=True, nullable=False)

    participants = db.relationship(
        "Participant", secondary=draw_subscription, backref="draws",
    )

    created_at = db.Column(
        db.DateTime, default=db.func.current_timestamp(), nullable=False
    )

    def __init__(self, in_process, responsible_number, description="", participants=[]):
        self.description = description
        self.in_process = in_process
        self.responsible_number = responsible_number
        self.participants = participants

    @staticmethod
    def create(responsible_number):
        draw = Draw(responsible_number=responsible_number, in_process=True)
        db.session.add(draw)

    def run(self):
        participants = copy.copy(self.participants)
        draw_result = []
        for participant in participants:
            names = copy.copy(participants)
            names.pop(names.index(participant))
            chosen = random.choice(list(set(participants) & set(names)))
            draw_result.append((participant, chosen))
            participants.pop(participants.index(chosen))
        return draw_result


class Participant(db.Model):
    """Participant"""

    __tablename__ = "participant"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    number = db.Column(db.String(120), unique=True, nullable=False)

    @staticmethod
    def find_or_create(name, number):
        participant = Participant.query.filter_by(number=number).first()
        if not participant:
            participant = Participant(name=name, number=number)
        return participant
