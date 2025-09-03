from authentication.models import User
from rest_framework.authtoken.models import Token


class UserLoginService(object):

    def __init__(self, username: str, password: str) -> None:
        self.username: str = username
        self.password: str = password
        self.user = self._user()

    def _user(self) -> User:
        user: User = None
        try:
            user = User.objects.get(username=self.username)
        except User.DoesNotExist as e:
            print("Error UserLoginService._user",e)
        return user

    def _validate_user(self) -> bool:
        return self.user.check_password(self.password)


    def perform_task_get_data(self) -> dict:
        response: dict = dict(success=False, error='invalid username.')
        if self.user:
            response = dict(success=False, error='invalid password.')
            if self._validate_user():
                data: dict = dict()
                token: Token = Token.objects.get_or_create(user=self.user)
                data['token'] = token[0].key
                response = dict(success=True, data=data)
        return response

