class Error(Exception):
    pass


class Unavailable(Error):
    pass


class APIError(Error):
    def __init__(self, message):
        self.message = message


class Refused(APIError):
    pass
