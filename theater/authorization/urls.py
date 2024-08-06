from django.urls import path
from authorization.views import registration, activate, site_login, site_logout

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('', site_login, name='site_login'),
    path('site_logout/', site_logout, name='site_logout'),
]