from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

list_of_cars = {'change oil': [], 'inflate tires': [], 'diagnostic': []}  # Task: Tickets
last_number = 0


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'menu.html')


class GetTicketView(View):
    def get(self, request, *args, **kwargs):
        global list_of_cars
        global last_number

        change_oil_queue = len(list_of_cars['change oil'])
        inflate_tires_queue = len(list_of_cars['inflate tires'])
        diagnostic_queue = len(list_of_cars['diagnostic'])

        if request.path_info == '/get_ticket/change_oil':
            task = 'change oil'
            waiting_time = change_oil_queue * 2
        elif request.path_info == '/get_ticket/inflate_tires':
            task = 'inflate tires'
            waiting_time = change_oil_queue * 2 + inflate_tires_queue * 5
        else:  # request.path_info == '/get_ticket/diagnostic':
            task = 'diagnostic'
            waiting_time = change_oil_queue * 2 + inflate_tires_queue * 5 + diagnostic_queue * 30

        last_number += 1
        list_of_cars[task].append(last_number)

        return HttpResponse(
            f'<div>Your number is {last_number}</div>\n'
            f'<div>Please wait around {waiting_time} minutes</div>')


class OperatorMenuView(View):
    def get(self, request, *args, **kwargs):
        global list_of_cars

        return render(request, 'processing.html', {'change_oil_queue': len(list_of_cars['change oil']),
                                                   'inflate_tires_queue': len(list_of_cars['inflate tires']),
                                                   'diagnostic_queue': len(list_of_cars['diagnostic'])})

    def post(self, request, *args, **kwargs):
        global list_of_cars

        for task in list_of_cars:
            if list_of_cars[task]:
                NextView.current_ticket = list_of_cars[task].pop(0)
                break

        return redirect('/processing')


class NextView(View):
    current_ticket = None

    def get(self, request, *args, **kwargs):
        global list_of_cars

        if NextView.current_ticket:
            return HttpResponse(f'<div>Next ticket #{NextView.current_ticket}</div>')

        return HttpResponse('<div>Waiting for the next client</div>')
