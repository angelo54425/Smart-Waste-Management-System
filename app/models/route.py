from datetime import date
from .db import db


class Route(db.Model):
    __tablename__ = "routes"

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # waste collection service ID
    route_name = db.Column(db.String(100), nullable=False)
    route_details = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Date, default=date.today)

    service = db.relationship(
        "User", backref=db.backref("collection_routes", lazy=True)
    )

    def __repr__(self):
        return f"<WasteCollectionRoute {self.route_name} for service {self.service_id}>"
