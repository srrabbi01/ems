from django.conf import settings
from django.urls import path, include
from api import views
urlpatterns = [
    path('get_service_data', views.admin_servicelist_view, name = 'get_service_data'),

    path('satus_update', views.satusUpdate, name = 'satusUpdate'),
    path('district', views.getDistrict_view, name = 'getDistrict'),
    path('upazila', views.getUpazila_view, name = 'getUpazila'),
    path('getEmail', views.getEmail_view, name = 'getEmail'),
    path('getPhone', views.getPhone_view, name = 'getPhone'),
    path('chat/send', views.sendChat_view, name = 'sendChat'),
    path('chat/receive', views.receiveChat_view, name = 'receiveChat'),
    path('map_api',views.map_api,name='map_api'),
    path('serviceNotify',views.serviceNotify_view,name='serviceNotify'),
    path('serviceAccept',views.serviceAccept_view,name='serviceAccept'),
    path('customerNotify',views.serviceAccept_customerNotify_view,name='customerNotify'),
    path('serviceinfo',views.getServiceInfo,name='serviceinfo'),
    path('servicereject',views.serviceReject,name='servicereject'),
]