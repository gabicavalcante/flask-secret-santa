from flask_sqlalchemy import SQLAlchemy
import copy
import random
from collections import deque

db = SQLAlchemy()


class SecretSanta(db.Model):
    __tablename__ = "secretsanta"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    in_process = db.Column(db.Boolean, nullable=True, default=False)
    creator_number = db.Column(db.String(120), unique=False, nullable=False)

    participants = db.relationship("Participant", backref="draws",)

    created_at = db.Column(
        db.DateTime, default=db.func.current_timestamp(), nullable=False
    )

    def __init__(self, in_process, creator_number, participants=[], result={}):
        self.in_process = in_process
        self.creator_number = creator_number
        self.participants = participants
        self.result = {}

    def __repr__(self):
        return f"SecretSanta: code={self.id}, responsible={self.creator_number} created={self.created_at}"

    @staticmethod
    def create(creator_number):
        ss = SecretSanta(in_process=True, creator_number=creator_number)
        return ss

    def run(self):
        participants = copy.copy(self.participants)
        random.shuffle(self.participants)

        partners = deque(participants)
        partners.rotate(1)
        result = list(zip(participants, partners))

        self.in_process = False
        return result


class Participant(db.Model):
    __tablename__ = "participant"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    number = db.Column(db.String(120), nullable=False)

    secretsanta_id = db.Column(db.Integer, db.ForeignKey("secretsanta.id"))

    def __repr__(self):
        return f"Participant: name={self.name}, number={self.number}"
