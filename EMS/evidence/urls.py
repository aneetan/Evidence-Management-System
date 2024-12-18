from django.urls import path
from . import views

urlpatterns = [
    path('', views.formLoad, name='formLoad'),
    path('save-to-ipfs/', views.save_to_ipfs, name='save_to_ipfs'),

]
