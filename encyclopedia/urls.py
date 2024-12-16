from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("new/", views.create, name="new"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("update/", views.update, name="update"),
    path("random/", views.randomize, name="random")
]
