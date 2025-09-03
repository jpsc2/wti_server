from rest_framework import serializers
from authentication.v1.services import user_login_service


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def perform_tasks_and_get_data(self) -> dict:
        response: dict = dict()
        try:
            response = user_login_service.UserLoginService(**self.validated_data).perform_task_get_data()
        except Exception as e:
            print('LoginSerializers.perform_tasks_and_get_data',e)
            response = {'error': e.__str__()}
        return response
