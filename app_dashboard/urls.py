from unicodedata import name
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views #import this
from . import views

urlpatterns = [
    path('', views.dashboard_view, name = 'dashboard'),
    path('update/<str:pk>', views.updateProfile_view, name = 'updateProfile'),
    path('change_password/', views.changePassword_view, name='changePassword'),
    path('request_service/', views.create_service_view, name = 'create_service'),
    path('service_request_list/', views.customerServiceRequestList_view, name = 'service_request_list'),
    path('work_request_list/', views.technicianServiceRequestList_view, name = 'technicianServiceList'),
    path('details/service/<str:pk>', views.details_service_view, name = 'details_service'),
    path('chat/', views.chat_view, name = 'chat'),
    path('customer_review/', views.customer_review_view, name = 'customer_review'),
    path('techmap/', views.techmap_view, name = 'techmap'),
    path('technician/payments/', views.technician_payments_view, name = 'technicianPayments'),
    path('customer/payments/', views.customer_payments_view, name = 'customerPayments'),

    path('send_invoice', views.admin_invoice_view, name = 'send_invoice'),
    path('get_technician_work_list/',views.get_technician_work_list,name='technician_work_list')
]