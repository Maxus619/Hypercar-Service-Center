from django.urls import path
from tickets.views import WelcomeView, MenuView, GetTicketView, OperatorMenuView, NextView

urlpatterns = [
    path('welcome/', WelcomeView.as_view()),
    path('menu/', MenuView.as_view()),
    path('get_ticket/change_oil', GetTicketView.as_view()),
    path('get_ticket/inflate_tires', GetTicketView.as_view()),
    path('get_ticket/diagnostic', GetTicketView.as_view()),
    path('processing/', OperatorMenuView.as_view()),
    path('next/', NextView.as_view()),
]
