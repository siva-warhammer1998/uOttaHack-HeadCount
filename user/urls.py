from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='user-home'),
    path('safety', views.safety, name='safety'),
    path('safety_reset', views.safety_reset, name='safety_reset'),   
    path('respond', views.respond, name='respond'),
    path('success', views.success, name='success'),
    path('push', views.push),   
    path('get_response', views.get_response, name='get_response'),   
]

