from django.urls import path
from . import views

urlpatterns = [
    path("webhooks/transactions/", views.transaction_listener, name="transaction_webhook"),
]