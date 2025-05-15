from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lights/', views.lights_view, name='lights'),
    path('curtains/', views.curtains_view, name='curtains'),
    path('pool/', views.pool_view, name='pool'),
    path('garage/', views.garage_view, name='garage'),
]
