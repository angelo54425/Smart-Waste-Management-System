from datetime import date
from .db import db


class Schedule(db.Model):
    __tablename__ = "schedules"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.Date, default=date.today)

    user = db.relationship("User", backref=db.backref("waste_schedules", lazy=True))

    def __repr__(self):
        return f"<WasteCollectionSchedule {self.id} for user {self.user_id}>"


class UpcomingCollection(db.Model):
    __tablename__ = "upcoming_collections"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    collection_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False, default="Pending")
    created_at = db.Column(db.Date, default=date.today)

    user = db.relationship(
        "User", backref=db.backref("upcoming_collections", lazy=True)
    )

    def __repr__(self):
        return f"<UpcomingCollection {self.collection_date} for user {self.user_id}>"
