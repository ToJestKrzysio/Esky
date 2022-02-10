from django.urls import path

from . import views

app_name = "search"
urlpatterns = [
    path('', views.SearchView.as_view(), name="search"),
    path('flights/', views.ResultsView.as_view(), name="flights"),
]
