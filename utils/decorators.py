# wraps decorator yazarken ası fonksiyonun kimliğini kaybetmesini önler

from flask import jsonify
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        role = claims.get("role")

        if role != "admin":
            return jsonify({"success": False, "message": "Admin access required"})

        return fn(*args, **kwargs)

    return wrapper
