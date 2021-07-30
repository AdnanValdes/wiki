from django.urls import path
from . import views


app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("random_page", views.random_page, name='random'),
    path("new", views.new, name='new'),
    path("edit/<str:title>/", views.edit, name='edit'),
    path('search', views.search, name='search'),
    path("<str:title>", views.entry, name='entry')
]
