from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic.base import RedirectView
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'accounts'

urlpatterns = [
    path('welcome/', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('search/', views.search, name='search'),
    path('feed/', views.feed, name='feed'),
    path('<username>/edit', views.edit_profile, name='edit'),
    path('<username>/following', views.following_list, name='my_friends'),
    path('<username>/', views.profile, name='profile'),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    )
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
