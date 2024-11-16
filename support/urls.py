# support/urls.py
from django.urls import path
from .views import TicketCreateView

urlpatterns = [
    path('support/tickets/', TicketCreateView.as_view(), name='create_ticket'),
]
