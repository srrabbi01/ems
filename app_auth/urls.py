from unicodedata import name
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views #import this
from . import views

urlpatterns = [
    path('login/', views.login_view, name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path('registration/', views.registration_view, name = 'registration'),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='app_auth/password_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app_auth/password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app_auth/password_reset/password_reset_complete.html'), name='password_reset_complete'),
]