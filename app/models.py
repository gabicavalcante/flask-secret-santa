from flask_sqlalchemy import SQLAlchemy
import copy
import random

db = SQLAlchemy()


class Draw(db.Model):
    """..."""

    __tablename__ = "draw"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    participants = db.relationship("Participant", back_populates="draw")
    draw_date = db.Column(
        db.DateTime, default=db.func.current_timestamp(), nullable=False
    )
    created_at = db.Column(
        db.DateTime, default=db.func.current_timestamp(), nullable=False
    )

    def secret_santa(self):
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
    name = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)

    draw_id = db.Column(db.Integer, db.ForeignKey("draw.id"))
    draw = db.relationship("Draw", back_populates="participants")
