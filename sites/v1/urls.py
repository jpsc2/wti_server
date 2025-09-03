from django.urls import path
from sites.v1.views import SitetList, SiteUpsert,SiteDelete

urlpatterns = [
    path('site_list/', SitetList.as_view(), name="PROJECT_GET_SITE_LIST"),
    path('site_upsert/', SiteUpsert.as_view(), name="PROJECT_GET_SITE_LIST"),
    path('site_delete/', SiteDelete.as_view(), name="DELETE_SITE"),
]
