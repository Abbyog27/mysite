from django.urls import path
from . import views  #right not, it has the index method

urlpatterns = [
    path("", views.index, name= "index"), 
]