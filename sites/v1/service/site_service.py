from authentication.models import User, UserCustomerMapping, UserSiteMapping, UserDeviceMapping
from sites.models import Site
from customers.models import Customer


class SiteListService(object):
    def __init__(self, user: User, attach_sub_item, customer_ids=None):
        self.user: User = user
        self.customer_ids = customer_ids or []
        self.attach_sub_item = attach_sub_item
        self.response = self._init_response()

    @staticmethod
    def _init_response():
        return {
            'success': False,
            'error': 'Server Error',
            'message': '',
        }

    def perform_task_and_get_data(self):
        site_list = []
        site_ids = []

        try:
            # ✅ check if user has direct customer mapping
            customer_mapping = UserCustomerMapping.objects.filter(
                user=self.user,
                customers__in=Customer.objects.filter(id__in=self.customer_ids)
            )
        except Exception as e:
            print('Error on SiteListService.perform_task_and_get_data (customer_mapping)', e)
            customer_mapping = []

        if customer_mapping.exists():
            try:
                site_ids.extend(
                    Site.objects.filter(customer_id__in=self.customer_ids).values_list('id', flat=True)
                )
            except Exception as e:
                print('Error on SiteListService.perform_task_and_get_data (site_ids from customer)', e)
        else:
            try:
                allowed_site_ids = UserSiteMapping.objects.filter(user=self.user).values_list('sites', flat=True)
                site_ids.extend(
                    Site.objects.filter(customer_id__in=self.customer_ids, id__in=allowed_site_ids).values_list('id', flat=True)
                )
            except Exception as e:
                print('Error on SiteListService.perform_task_and_get_data (site_ids from mapping)', e)

        try:
            # ✅ also include sites from device mapping
            device_list = UserDeviceMapping.objects.get(user=self.user).devices.select_related("site__customer").all()
            for device in device_list:
                if device.site.customer.id in self.customer_ids:
                    site_ids.append(device.site.id)
        except Exception as e:
            print('Error in SiteListService.device_list', e)

        # ✅ optimized query: select_related("customer")
        sites_objects = (
            Site.objects
            .filter(id__in=site_ids)
            .select_related("customer")
            .only("id", "name", "description", "customer__id", "customer__name")
        )

        for site in sites_objects:
            project = {
                "id": site.id,
                "name": site.name,
                "description": site.description,
                "customer": {
                    "id": site.customer.id,
                    "name": site.customer.name,
                },
                "device_list": []
            }
            # If needed later: attach_sub_item can call DevicesListService
            # if self.attach_sub_item:
            #     project['device_list'] = DevicesListService(user=self.user, site_ids=[site.id]).perform_task_and_get_data()

            site_list.append(project)

        return site_list


class SiteUpsert(object):
    def __init__(self, id, name, description, customer_id):
        self.id = id
        self.name = name
        self.description = description
        self.customer_id = customer_id
        self.response = self._init_response()

    @staticmethod
    def _init_response():
        return {"success": False, "error": "Server Error", "message": ""}

    def _update_Site_model(self):
        try:
            site_object = Site.objects.get(id=self.id)
            if self.name:
                site_object.name = self.name
            if self.customer_id:
                site_object.customer_id = self.customer_id
            if self.description:
                site_object.description = self.description
            site_object.save()
            self.response["success"] = True
            self.response["message"] = "Site is updated successfully."
        except Exception as e:
            print("Error on SiteUpsert._update_Site_model due to ", e)
            self.response["error"] = str(e)

    def _create_Site_object(self):
        try:
            Site.objects.create(
                name=self.name, description=self.description, customer_id=self.customer_id
            )
            self.response["success"] = True
            self.response["message"] = "Site is created successfully."
        except Exception as e:
            print("Error on SiteUpsert._create_Site_object due to ", e)
            self.response["error"] = str(e)

    def upsert(self):
        if self.id:
            self._update_Site_model()
        else:
            self._create_Site_object()
        return self.response


class SiteDelete(object):
    def __init__(self, site_id):
        self.site_id = site_id
        self.response = self._init_response()

    @staticmethod
    def _init_response():
        return {"success": False, "error": "Server Error", "message": ""}

    def delete(self):
        try:
            site_object: Site = Site.objects.get(id=self.site_id)
            site_object.delete()
            self.response["success"] = True
            self.response["message"] = "Site is deleted successfully."
        except Exception as e:
            print("Error on SiteDelete.delete due to ", e)
            self.response["error"] = str(e)
        return self.response
