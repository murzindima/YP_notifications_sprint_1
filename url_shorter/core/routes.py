import re
import string
import uuid
from datetime import datetime, timedelta
from random import choice

from flask import request, redirect, jsonify, abort

from core import app, db
from core.models import ShortUrls


def generate_short_id(num_of_chars: int):
    """Function to generate short_id of specified number of characters"""
    return "".join(
        choice(string.ascii_letters + string.digits)
        for _ in range(num_of_chars)
    )


def generate_expire_date(days):
    """Generate expiration date"""
    return datetime.now() + timedelta(days=days)


def is_valid_url(url):
    """Check url format."""
    url_pattern = re.compile(
        r"^(?:http|ftp)s?://"  # Schema (http, https, ftp)
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domen...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or IP
        r"(?::\d+)?"  # port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return re.match(url_pattern, url) is not None


@app.route("/s/", methods=["POST"])
def create_short_url():
    if request.method == "POST":
        data = request.json
        redirect_url = data.get("redirect_url")
        user_id = data.get("user_id")
        expire_days = data.get("expire_days")

        if not redirect_url:
            return jsonify({"status": "The URL is required!"}), 400

        if not is_valid_url(redirect_url):
            return jsonify({"status": "Invalid url format!"}), 400

        if not user_id:
            return jsonify({"status": "The UserId is required!"}), 400

        try:
            uuid.UUID(user_id)
        except ValueError:
            return jsonify({"status": "Invalid UserId format!"}), 400

        short_id = generate_short_id(8)

        # if short_id already exist
        while ShortUrls.query.filter_by(short_id=short_id).first():
            short_id = generate_short_id(8)

        if not expire_days:
            expire_days = 7

        expire_at = generate_expire_date(expire_days)

        new_link = ShortUrls(
            redirect_url=redirect_url,
            short_id=short_id,
            user_id=user_id,
            expire_at=expire_at,
            created_at=datetime.now(),
        )
        db.session.add(new_link)
        db.session.commit()
        short_url = request.url_root + "s/" + short_id

        return jsonify({"short_url": short_url}), 200

    return jsonify({"status": "Method Not Allowed"}), 405


@app.route("/s/<short_id>", methods=["GET"])
def confirm_email(short_id):
    link = ShortUrls.query.filter_by(short_id=short_id).first()
    if link:
        if link.expire_at >= datetime.now():
            # здесь надо реализовать логику подтверждения e-mail
            print(link.user_id)
            return redirect(link.redirect_url)
        else:
            abort(404, description="Expired URL")
    else:
        abort(404, description="Invalid URL")


# запуск этого метода можно добавить в cron по рассписанию.
@app.route("/s/", methods=["DELETE"])
def delete_expired_links():
    expired_links = ShortUrls.query.filter(
        ShortUrls.expire_at < datetime.now()
    ).all()
    for link in expired_links:
        db.session.delete(link)
    db.session.commit()

    return jsonify({"status": "Expired links deleted successfully"}), 200
