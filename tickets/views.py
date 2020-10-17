from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

wellcome = "Welcome to the Hypercar Service!"
options = [
    "Change oil",
    "Inflate tires",
    "Get diagnostic test",
]
opt_one = 'Change oil'
opt_two = 'Inflate tires'
opt_three = 'Get diagnostic test'

page_one = 'change_oil'
page_two = 'inflate_tires'
page_three = 'diagnostic'

ticket_number = 0
line_of_cars = {
    'change_oil': [],
    'inflate_tires': [],
    'diagnostic': [],
}
ticket = None

def handler(flag):
    global ticket_number
    ticket_number += 1
    global line_of_cars
    if flag == 1:
        total = len(line_of_cars['change_oil']) * 2
        line_of_cars['change_oil'].append(ticket_number)
    elif flag == 2:
        total = len(line_of_cars['inflate_tires']) * 5 + len(line_of_cars['change_oil']) * 2
        line_of_cars['inflate_tires'].append(ticket_number)
    else:
        total = len(line_of_cars['inflate_tires']) * 5 + len(line_of_cars['change_oil']) * 2 + \
                len(line_of_cars['diagnostic']) * 30
        line_of_cars['diagnostic'].append(ticket_number)
    return total


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        context = {"options": options, "wellcome": wellcome, 'page_one': page_one, 'page_two': page_two,
                   'page_three': page_three, 'opt_two': opt_two, 'opt_one': opt_one, 'opt_three': opt_three}
        return render(request, "tickets/menu.html", context=context)


class OilView(View):
    def get(self, request, *args, **kwargs):
        total = handler(flag=1)
        return render(request, "tickets/common.html", context={"total": total, "ticket_number": ticket_number})


class TiresView(View):
    def get(self, request, *args, **kwargs):
        total = handler(flag=2)
        return render(request, "tickets/common.html", context={"total": total, "ticket_number": ticket_number})


class DiagnosticView(View):
    def get(self, request, *args, **kwargs):
        total = handler(flag=3)
        return render(request, "tickets/common.html", context={"total": total, "ticket_number": ticket_number})

class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        context = {'oil': len(line_of_cars['change_oil']), 'tires': len(line_of_cars['inflate_tires']),
                   'diagnostic': len(line_of_cars['diagnostic'])}
        return render(request, "tickets/processing.html", context=context)
    def post(self, request, *args, **kwargs):
        global ticket
        if len(line_of_cars['change_oil']):
            ticket = line_of_cars['change_oil'].pop(0)
        elif len(line_of_cars['inflate_tires']):
            ticket = line_of_cars['inflate_tires'].pop(0)
        elif len(line_of_cars['diagnostic']):
            ticket = line_of_cars['diagnostic'].pop(0)
        return redirect('/next')


class NextView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/next.html', context={'ticket': ticket})


# class PostHandler(View):
#     def post(self, request, *args, **kwargs):
#         return redirect('/next')