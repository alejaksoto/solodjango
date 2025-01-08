from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('embedded-callback/', views.embedded_callback, name='embedded_callback'),
    path('welcome/', views.index, name='index'),
    path('whatsapp/', views.whatsapp_verify, name='whatsapp_verify'),
    
]