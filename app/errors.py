class UserNotFoundError(Exception):
    def __init__(self, username):
        super().__init__(f'User Not Found, username: {username}')


class UserAlreadyExistsError(Exception):
    def __init__(self, username):
        super().__init__(f'User Already Exists, username: {username}')
