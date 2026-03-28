from django.urls import path
from . import views

urlpatterns = [
    # 🔥 ROOT ROUTE (CRITICAL FOR AWS HEALTH CHECK)
    path("", views.home, name="home"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # Ride operations
    path("rides/", views.ridelist, name="ridelist"),
    path("rides/create/", views.createride, name="createride"),
    path("rides/update/<int:id>/", views.updateride, name="updateride"),
    path("rides/delete/<int:id>/", views.deleteride, name="deleteride"),

    # Search
    path("search/", views.searchride, name="searchride"),
]