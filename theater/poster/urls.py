from django.urls import path

from poster import views

urlpatterns = [
    path('', views.RepertoireView.as_view(), name="repertoire"),
    path('<slug:slug>/', views.PerformanceSessionsView.as_view(), name="performance_sessions"),
    path('afisha', views.AfishaView.as_view(), name='afisha'),
]
