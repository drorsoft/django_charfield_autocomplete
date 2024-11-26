from django.urls import path
from . import views

urlpatterns = [
    path('autocomplete/', views.admin_autocomplete, name='admin_autocomplete'),
]
