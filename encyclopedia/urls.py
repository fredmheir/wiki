from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage",views.newpage, name="newpage"),
    path("search", views.search, name="search"),
    path("random", views.randomPage, name="random"),
    path("edit<str:entrytitle>", views.editEntry, name="edit"),
    path("<str:entrytitle>",views.entry, name="entry"),

]
