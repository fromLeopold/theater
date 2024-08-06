from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin_page/', include("admin_panel.urls")),
    path('', include("theater_info.urls")),
    path('authorization/', include("authorization.urls")),
    path('repertoire/', include("poster.urls")),
    path('ticket_buy/', include("ticket_buy.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
