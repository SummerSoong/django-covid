from django.urls import path
from . import views

urlpatterns = [
	path("", views.redirect_to_home), # redirect "/" to "home"
	path("home", views.home),
	path("statistics", views.statistics),
	path("contact", views.contact)
]
