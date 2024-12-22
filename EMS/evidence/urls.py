from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add, name='add'),
    path('view/', views.view, name='view'),
    path('save-to-ipfs/', views.save_to_ipfs, name='save_to_ipfs'),
    path('process_ipfs/', views.process_ipfs, name='process_ipfs'),

]
