from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='user-home'),
    path('safety', views.safety, name='safety'),
    path('respond', views.respond, name='respond'),
    path('success', views.success, name='success'),
    path('send_push', views.send_push),
    path('push', views.push),   
    path('get_response', views.get_response),   
]

