from authentication.models import User


class UserDataService(object):

    def __init__(self, user: User) -> None:
        self.user = user

    def _user_data(self) -> dict:
        user_data: dict = dict(
            id= self.user.id,
            name=self.user.first_name +' '+self.user.last_name,
            username=self.user.username,
            email=self.user.email,
            is_admin=self.user.is_superuser,
            is_staff=self.user.is_staff
        )
        return user_data

    def perform_task_get_data(self) -> dict:
        data: dict = self._user_data()
        return data

