from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from tours import data
from django.http import HttpResponse, HttpResponseNotFound, Http404
import random


# Create your views here.

def get_town(departure):
    town = ''
    if departure == 'msk':
        town = "Москвы"
    elif departure == 'spb':
        town = "Питера"
    elif departure == 'kazan':
        town = "Казани"
    elif departure == 'nsk':
        town = "Новосибирска"
    elif departure == 'ekb':
        town = "Екатеринбурга"
    return town


# def custom_handler404(request, exception=None):
#     return HttpResponseNotFound('Ой, что то сломалось... !')
#
#
# def custom_handler500(request, exception=None):
#     return HttpResponseNotFound('Ой, что то сломалось... !')


class MainView(View):



    def get(self, request, *args, **kwargs):
        tours = {i: data.tours[i] for i in
                 random.sample(range(1, len(data.tours)), 6)}

        context = {
            'tours': tours,
        }
        return render(request, 'index.html', context)


class DepartureView(View):

    def get(self, request, departure, *args, **kwargs):

        set_departure = {value.get('departure') for (key, value) in data.tours.items()}
        # if departure not in set_departure:
        #     return HttpResponseNotFound('Ой, что то сломалось... !')

        tours = {key: value for (key, value) in data.tours.items()
                 if value['departure'] == departure}

        town = get_town(departure)
        array_price = []
        array_nights = []

        for keys, value in tours.items():
            array_price.append(value['price'])
            array_nights.append(value['nights'])

        min_price = min(array_price)
        max_price = max(array_price)
        min_nights = min(array_nights)
        max_nights = max(array_nights)
        count_tours = len(array_price)

        context = {
            'tours': tours,
            'town': town,
            'min_price': min_price,
            'max_price': max_price,
            'min_nights': min_nights,
            'max_nights': max_nights,
            'count_tours': count_tours
        }

        return render(request, 'departure.html', context)


class TourView(View):
    def get(self, request, id):
        # if id not in data.tours:
        #     return HttpResponseNotFound('Ой, что то сломалось... !')


        tour = data.tours[id]
        departure = data.tours[id]["departure"]

        town = get_town(departure)


        context = {'tour': tour,
                   'departure': departure,
                   'town': town}
        return render(request, 'tour.html', context)
