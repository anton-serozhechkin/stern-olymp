from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sore.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# its works only when debug=False
handler404 = 'sore.views.not_found_view'
handler500 = 'sore.views.error_view'
handler403 = 'sore.views.permission_denied_view'
handler400 = 'sore.views.bad_request_view'