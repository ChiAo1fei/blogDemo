"""__author__ == ChiAo"""
from functools import wraps

from flask import session, redirect, url_for


def is_login(func):

    @wraps(func)
    def check():
        try:
            session['login_status']
            return func()
        except:
            return redirect(url_for('first.login'))

    return check
