from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from app_index.views import index_view
handler404 = 'app_dashboard.views.custom_page_not_found_view'

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'),name="api"),
    path('dashboard/', include('app_dashboard.urls'),name="app_dashboard"),
    path('auth/', include('app_auth.urls'),name="app_auth"),
    path('', index_view, name = 'home'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
