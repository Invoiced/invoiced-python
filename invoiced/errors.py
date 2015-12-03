class ErrorBase(Exception):
    def __init__(self, message=None, status_code=None, error=None):
        super(ErrorBase, self).__init__(message)

        self._message = message
        self.status_code = status_code
        self.error = error

    def __str__(self):
        return "({0}): {1}".format(self.status_code, self._message)


class ApiConnectionError(ErrorBase):
    pass


class ApiError(ErrorBase):
    pass


class InvalidRequestError(ErrorBase):
    pass


class AuthenticationError(ErrorBase):
    pass
