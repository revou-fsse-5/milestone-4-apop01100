from flask import jsonify
from functools import wraps
from app.constant.messages import Messages
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.users_model import User
from app.connections.db import Session

# Custom decorator to check role
def role_required(*role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated_view(*args, **kwargs):
            payload = get_jwt_identity()
            with Session() as session:
                if payload["role"] not in role:
                    return jsonify({"message": Messages.ROLE_NOT_AUTHORIZED}), 403
                
                user = session.query(User).filter_by(username = payload["username"])
                if user is None:
                    return jsonify({"message": Messages.USERNAME_NOT_FOUND}), 404
            return fn(payload, *args, **kwargs)
        return decorated_view
    return wrapper