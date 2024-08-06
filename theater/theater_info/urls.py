from django.urls import path

from theater_info import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('theater_contacts/', views.TheaterInfoView.as_view(), name='theater_contacts'),
    path('troupe', views.TroupeView.as_view(), name='troupe'),
    path('troupe/<int:pk>', views.TroupeMemberView.as_view(), name='troupe_member_details'),
]
