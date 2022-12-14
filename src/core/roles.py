from functools import wraps
from flask import redirect, url_for
from flask_login import current_user


def role_required(role_value: int, redirect_endpoint: str = 'auth.login'):
    def decorator(func):
        @wraps(func)
        def authorize(*args, **kwargs):
            if current_user.role < role_value:
                return redirect(url_for(redirect_endpoint))
            return func(*args, **kwargs)
        return authorize
    return decorator


def role_names(role: str) -> int:
    roles = {
        'admin': 2,
        'moderator': 1,
        'user': 0
    }
    return roles.get(role, 0)
