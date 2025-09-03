from django.contrib.auth.models import User


class UserListService(object):

    def __init__(self, user: User, ):
        self.user: User = user

    def perform_task_and_get_data(self):
        users_list = []
        users = User.objects.all()
        for user in users:
            user: User = user
            data = {
                "id": user.id,
                "name": user.first_name + ' ' + user.last_name,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "is_admin": user.is_superuser,
                "is_staff": user.is_staff}
            users_list.append(data)
        return users_list


class UserUpsert(object):

    def __init__(self, id, name, username, is_admin, password):
        self.id = id
        self.name = name
        self.username = username
        self.is_admin = is_admin
        self.password = password
        self.response = self._init_response()

    @staticmethod
    def _init_response():
        return {
            'success': False,
            'error': 'Server Error',
            'message': '',
        }

    def _update_user_model(self):
        try:
            user_object: User = User.objects.get(id=self.id)
            if self.name:
                user_object.first_name = self.name
            if self.username:
                user_object.customer_id = self.username
            if self.is_admin:
                user_object.is_admin = self.is_admin
            if self.password:
                user_object.set_password(self.password)
            user_object.save()
            self.response['success'] = True
            self.response['message'] = 'user is updated successfully.'
        except Exception as e:
            print('Error on UserUpsert._update_user_model due to ', e)
            self.response['error'] = str(e)

    def _create_device_object(self):
        try:
            user_object = User.objects.create(
                first_name=self.name,
                username=self.username,
            )
            user_object.set_password(self.password)
            user_object.is_admin = self.is_admin
            user_object.save()
            self.response['success'] = True
            self.response['message'] = 'user is created successfully.'
        except Exception as e:
            print('Error on UserUpsert._update_user_model due to ', e)
            self.response['error'] = str(e)

    def upsert(self):
        if not self.username:
            self.response['error'] = 'Please enter a valid username.'
            return self.response
        if self.id:
            self._update_user_model()
        else:
            self._create_device_object()
        return self.response


class UserDelete(object):

    def __init__(self, user_id):
        self.user_id = user_id
        self.response = self._init_response()

    @staticmethod
    def _init_response():
        return {
            'success': False,
            'error': 'Server Error',
            'message': '',
        }

    def delete(self):
        try:
            print("id", self.user_id)
            user_object: User = User.objects.get(id=self.user_id)
            user_object.delete()
            self.response['success'] = True
            self.response['message'] = 'user is deleted successfully.'
        except Exception as e:
            print('Error on UserDelete._update_user_model due to ', e)
            self.response['error'] = str(e)

        return  self.response
