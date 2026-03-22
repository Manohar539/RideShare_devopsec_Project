from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("rides/", views.ridelist, name="ridelist"),
    path("create/", views.createride, name="createride"),
    path("update/<int:id>/", views.updateride, name="updateride"),
    path("delete/<int:id>/", views.deleteride, name="deleteride"),
    path("search/", views.searchride, name="searchride"),
    path("dashboard/", views.dashboard, name="dashboard"),
]