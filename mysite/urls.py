from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView

urlpatterns = [
    path('/', RedirectView.as_view(url='/me/welcome')),
    path('me/', include('accounts.urls', namespace='accounts')),
    path('admin/', admin.site.urls),
    path("favicon.ico", RedirectView.as_view(url="static/favicon.ico"))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
