from django.contrib.auth.models import User
from authentication.models import UserCustomerMapping, UserSiteMapping, UserDeviceMapping
from customers.models import Customer
from sites.v1.service import site_service


class CustomerListService(object):
    def __init__(self, user: User, attach_sub_item):
        self.user: User = user
        self.attach_sub_item = attach_sub_item

    def _customer_list(self):
        customer_set = set()
        customer_list_data = {}

        try:
            mapping = UserCustomerMapping.objects.filter(user=self.user).first()
            if mapping:
                customer_objects = mapping.customers.only("id", "name", "email", "phone_number")
                customer_set.update(customer_objects)
        except Exception as e:
            print("Error in CustomerListService._customer_list", e)

        try:
            mapping = UserSiteMapping.objects.filter(user=self.user).first()
            if mapping:
                site_objects = (
                    mapping.sites
                    .select_related("customer")
                    .only("id", "name", "customer__id", "customer__name", "customer__email", "customer__phone_number")
                )
                customer_set.update([s.customer for s in site_objects])
        except Exception as e:
            print("Error in CustomerListService._site_list", e)

        try:
            mapping = UserDeviceMapping.objects.filter(user=self.user).first()
            if mapping:
                device_objects = (
                    mapping.devices
                    .select_related("site__customer")
                    .only("id", "name", "site__id", "site__customer__id", "site__customer__name")
                )
                customer_set.update([d.site.customer for d in device_objects if d.site and d.site.customer])
        except Exception as e:
            print("Error in CustomerListService._device_list", e)

        for customer_object in customer_set:
            customer = {
                "id": customer_object.id,
                "name": customer_object.name,
                "email": customer_object.email,
                "phone_number": customer_object.phone_number,
                "site_list": []
            }
            if self.attach_sub_item:
                customer["site_list"] = site_service.SiteListService(
                    user=self.user,
                    customer_ids=[customer_object.id],
                    attach_sub_item=self.attach_sub_item,
                ).perform_task_and_get_data()
            customer_list_data[customer_object.id] = customer

        # Convert to list before returning
        return list(customer_list_data.values())

    def perform_task_and_get_data(self):
        return self._customer_list()

class CustomerUpsert(object):
    def __init__(self, id, name, email, phone_number, description, user):
        self.id = id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.description = description
        self.user = user
        self.response = self._init_response()

    @staticmethod
    def _init_response():
        return {
            'success': False,
            'error': 'Server Error',
            'message': '',
        }

    def _update_customer_model(self):
        try:
            customer_object = Customer.objects.get(id=self.id)
            if self.name:
                customer_object.name = self.name
            if self.email:
                customer_object.email = self.email
            if self.phone_number:
                customer_object.phone_number = self.phone_number
            if self.description:
                customer_object.description = self.description
            customer_object.save()
            self.response['success'] = True
            self.response['message'] = 'customer is updated successfully.'
        except Exception as e:
            print('Error on CustomerUpsert._update_user_model due to ', e)
            self.response['error'] = str(e)

    def _create_customer_object(self):
        try:
            Customer.objects.create(
                name=self.name,
                email=self.email,
                phone_number=self.phone_number,
                description=self.description,
            )
            self.response['success'] = True
            self.response['message'] = 'customer is created successfully.'
        except Exception as e:
            print('Error on CustomerUpsert._update_user_model due to ', e)
            self.response['error'] = str(e)

    def _map_from_object(self, customer_object):
        customer: dict = {
            "id": customer_object.id,
            "name": customer_object.name,
            "email": customer_object.email,
            "phone_number": customer_object.phone_number,
            "site_list": []
        }
        return customer

    def upsert(self):
        if self.id:
            self._update_customer_model()
        else:
            self._create_customer_object()
        return self.response


class CustomerDelete(object):
    def __init__(self, customer_id):
        self.customer_id = customer_id
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
            customer_object: User = Customer.objects.get(id=self.customer_id)
            customer_object.delete()
            self.response['success'] = True
            self.response['message'] = 'customer is deleted successfully.'
        except Exception as e:
            print('device on CustomerDelete.delete due to ', e)
            self.response['error'] = str(e)
        return self.response
