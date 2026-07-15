import os
from flask import request
import jwt


def token_verification():
    token = request.headers.get("Authorization")

    if not token:
        return None

    try:
        decoded = jwt.decode(
            token,
            os.getenv("JWT_SECRET"),
            algorithms=["HS256"]
        )

        return decoded

    except jwt.InvalidTokenError:
        return None