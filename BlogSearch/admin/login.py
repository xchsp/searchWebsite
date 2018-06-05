from functools import wraps
from flask import session,url_for, redirect,logging


def logincheck(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            if 'login' in session:
                if session['login'] == 'login':
                    return f(*args, **kwargs)
                else:
                    return redirect(url_for('.login'))
            else:
                return redirect(url_for('.login'))
        except Exception:
            pass
            return redirect(url_for('.login'))

    return wrapper
