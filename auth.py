"""
PR 2160 proposal for auth hierarchy

After the detailed dsicussion, we should probalby implement something like:
https://docs.python-requests.org/en/latest/user/authentication/#new-forms-of-authentication
"""

class AuthBase:
    uses_sessions = False
    _cached_auth = None
    _session = None
    config = None

    def __init__(self, config):
        self.config = config

    def _perform_auth(self):
        raise NotImplementedError

    @property
    def session(self):
        if self._session:
            return self._session

        with lock:
            # returns None for no session, or expired session
            self._session = self._load_session_from_file()
            if self._session:
                return self._session

            self._session = self.get_new_session()
            self._save_session(session_file, self._session)
            return self._session

    def _auth_with_session(self, parameters):
        parameters.setdefault("cookies", {})
        cookies = parameters.get("cookies")
        cookies["session"] = self.session["session"]

    def authenticate_parameters(self, parameters):
        if self.uses_sessions:
            self._auth_with_session(parameters)
            return
        self.set_auth_argument(parameters)

    def set_auth_argument(self, parameters):
        """ Implemented for Login+Token """
        raise NotImplementedError

    def get_new_session():
        """ Implemented for GSSAPI or OIDC """
        raise NotImplementedError

    def reauth(self):
        """
        If Request detects authentication error, we can invalidate the caches
        (session, or so) and before the next attempt (see connection_attempts)
        we will re-authenticate.
        """
        if self.uses_sessions:
            with lock:
                """ remove the session cookie file """
            self._session = None
        raise CoprAuthError("can't re-authenticate with this method")


    class GSSAPIAuth(AuthBase):
        uses_sessions = True
        def get_new_session():
            """ TO BE IMPLEMENTED """
            pass


    class TokenAuth(AuthBase):
        def set_auth_argument(self, parameters):
            parameters["auth"] = self.config["login"], self.config["token"]
