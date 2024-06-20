from datetime import date
from .db import db


class RecyclingTracker(db.Model):
    __tablename__ = "recycling_tracker"

    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey("upcoming_collections.id"))
    material = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    impact_score = db.Column(db.Float, nullable=False)
    waste_category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.Date, default=date.today)

    collection = db.relationship(
        "UpcomingCollection", backref=db.backref("recycling_tracker", lazy=True)
    )

    def __repr__(self):
        return f"<RecyclingTracker {self.id} for schedule {self.schedule_id}>"
