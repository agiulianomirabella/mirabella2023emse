from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("validity", views.validity, name="validity"),
    path("uncertainty", views.uncertainty, name="uncertainty"),
    path("train", views.train, name="train"),
]