from functools import wraps
from flask import g, request, redirect, session

class AccountSession():
    storage_key = ""
    base_path = "/"

    def get_identifier(self):
        if self.is_authenticated():
            return session[self.storage_key]

        return "err"

    def configure_context(self, session_store, app_globals):
        app_globals.user = 0

        if self.is_authenticated():
            app_globals.user = session[self.storage_key]

    def is_authenticated(self):
        if self.storage_key in session and session[self.storage_key] and session[self.storage_key] > 0:
            return True

        return False

    def auth_required(self, route_handler, fallback_url="signin"):
        @wraps(route_handler)
        def wrapper_routine(*arguments, **keyword_arguments):
            if self.storage_key not in session or session[self.storage_key] is None:
                print(fallback_url)
                return redirect(self.base_path + fallback_url)
            return route_handler(*arguments, **keyword_arguments)
        return wrapper_routine

    def guest_only(self, route_handler, redirect_target="/"):
        @wraps(route_handler)
        def wrapper_routine(*arguments, **keyword_arguments):
            if self.storage_key in session and session[self.storage_key] is not None:
                return redirect(self.base_path + redirect_target)
            return route_handler(*arguments, **keyword_arguments)
        return wrapper_routine

    def terminate_session(self):
        session[self.storage_key] = None

    def authenticate(self):
        pass