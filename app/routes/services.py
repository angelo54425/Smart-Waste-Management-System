# Import necessary modules and models
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.decorators.decorators import role_required
from app.models.user import User
from app.models.db import db
from app.forms import CollectionForm
from app.models import UpcomingCollection, RecyclingTracker

# Define the service blueprint
service_bp = Blueprint("service", __name__)

BASE_IMPACT_FACTORS = {
    "plastic": 1.2,
    "glass": 0.8,
    "metal": 1.5,
    "paper": 1.0,
}


@service_bp.route("/collections", methods=["GET"])
@login_required
@role_required("service-man")
def view_collections():
    collections = (
        UpcomingCollection.query.join(User, User.id == UpcomingCollection.user_id)
        .order_by(UpcomingCollection.collection_date)
        .all()
    )
    tracks = RecyclingTracker.query.all()

    total_waste_collected = sum(track.quantity for track in tracks)
    total_completed_schedules = UpcomingCollection.query.filter_by(
        status="Completed"
    ).count()
    total_cancelled_schedules = UpcomingCollection.query.filter_by(
        status="Cancelled"
    ).count()

    return render_template(
        "collections.html",
        collections=collections,
        tracks=tracks,
        total_waste_collected=total_waste_collected,
        total_completed_schedules=total_completed_schedules,
        total_cancelled_schedules=total_cancelled_schedules,
    )


@service_bp.route("/collections/cancel/<int:collection_id>", methods=["GET"])
@login_required
@role_required("service-man")
def cancel_collection(collection_id):
    collection = UpcomingCollection.query.get_or_404(collection_id)
    collection.status = "Cancelled"
    db.session.commit()
    flash("Collection cancelled successfully.", "success")
    return redirect(url_for("service.view_collections"))


@service_bp.route("/collections/collect/<int:collection_id>", methods=["GET", "POST"])
@login_required
@role_required("service-man")
def collect_garbage(collection_id):
    collection = UpcomingCollection.query.get_or_404(collection_id)
    form = CollectionForm()
    if form.validate_on_submit():
        material = form.material.data
        quantity = form.quantity.data
        base_impact_factor = BASE_IMPACT_FACTORS.get(material, 1.0)
        impact_score = quantity * base_impact_factor

        tracker = RecyclingTracker(
            collection_id=collection.id,
            material=material,
            quantity=quantity,
            impact_score=impact_score,
            waste_category=form.waste_category.data,
        )
        collection.status = "Completed"
        db.session.add(tracker)
        db.session.commit()
        flash("Garbage collected and recorded successfully.", "success")
        return redirect(url_for("service.view_collections"))
    return render_template("collect.html", form=form, collection=collection)
