from django.contrib.auth.decorators import user_passes_test
from django.urls import path, reverse_lazy
from django.contrib import admin

from theater_info.core_utils import admin_check
from . import views

urlpatterns = [
    path('data_base/', admin.site.urls),
    path('', views.AdminPanelView.as_view(), name='admin_page'),
    path('download/', views.AdminPanelView.as_view(), name='admin_panel_download'),
]

