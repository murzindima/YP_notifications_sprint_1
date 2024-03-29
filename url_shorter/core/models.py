from datetime import datetime

from core import db


class ShortUrls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    redirect_url = db.Column(db.String(500), nullable=False)
    short_id = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(
        db.DateTime(), default=datetime.now(), nullable=False
    )
    user_id = db.Column(db.String(36), nullable=False)
    expire_at = db.Column(db.DateTime(), nullable=False)
