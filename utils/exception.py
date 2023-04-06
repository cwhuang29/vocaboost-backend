class AuthException(Exception):
    pass


class WordException(Exception):
    pass


class UserDoesNotExistError(AuthException):
    def __init__(self):
        self.status_code = 400
        self.detail = 'This user does not exist'


class UserAlreadyExistError(AuthException):
    def __init__(self):
        self.status_code = 409
        self.detail = 'This user already exists'


class LoginMethodError(AuthException):
    def __init__(self):
        self.status_code = 400
        self.detail = 'The login method is not supported yet'


class ManageWordActionError(WordException):
    def __init__(self):
        self.status_code = 400
        self.detail = 'The action should be either add or remove'


class WordNotFoundError(WordException):
    def __init__(self):
        self.status_code = 400
        self.detail = 'This word does not exist'
