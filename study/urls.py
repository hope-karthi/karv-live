from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .import settings as setting
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('baseapp.urls')),
    path('api/',include('baseapp.api.urls'))
]

urlpatterns += static(setting.MEDIA_URL, document_root=setting.MEDIA_ROOT)
