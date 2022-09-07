class GraphQLError(Exception):
    def __init__(self, message, error_type="GraphQLError"):
        self.error_message = message
        self.error_type = error_type
        super(GraphQLError, self).__init__(self.error_message)


class AuthorizationError(Exception):
    def __init__(self, error_message):
        self.error_message = (
            error_message if error_message else "Not Authorized"
        )
        self.error_type = "AUTHORIZATION_ERROR"
        super(AuthorizationError, self).__init__(self.error_message)


class MissingJWTError(Exception):
    def __init__(self, error_message):
        self.error_message = (
            error_message if error_message else "Missing Authorization JWT"
        )
        self.error_type = "MissingJWTError"
        super(MissingJWTError, self).__init__(self.error_message)


class NotFoundError(Exception):
    def __init__(self, error_message):
        self.error_message = error_message if error_message else "Not Found"
        self.error_type = "NotFoundError"
        super(NotFoundError, self).__init__(self.error_message)
