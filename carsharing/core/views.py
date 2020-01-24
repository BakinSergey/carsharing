import json

from core.utils import *
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView, View
from django.utils.safestring import mark_safe

from django.core.serializers.json import DjangoJSONEncoder
from django.core import management

from core.models import Car, ExteriorGallery, InteriorGallery
from random import choice

# Create your views here.


fa_icons = ["fa fa-spinner fa-spin fa-fw",
            "fa fa-circle-o-notch fa-spin fa-fw",
            "fa fa-refresh fa-spin fa-fw",
            "fa fa-cog fa-spin fa-fw",
            "fa fa-spinner fa-pulse fa-fw"
            ]

fa_icons_2 = [
    "fa-home",
    "fa-book",
    "fa-pencil"
]


def prepare_car_info(car_list):

    # gather data about all cars
    drop_items = []
    swal_items = []
    drop_items_info = {}
    for car in car_list:
        car_color = get_color(car.params['color'])
        item = f'<button class="dropdown-item" type="button" id={car.pk}>' \
               f'<i class="fa fa-car" style="color:{car_color}"></i>&nbsp{car.params["model"]}</button>'

        swal_item = f'<i class="fa fa-car fa-3x" style="color:{car_color}"></i>' \
                    f'<p>модель: <b>{car.params["model"]}</b>, цвет: <b>{car_color}</b>, год выпуска: <b>{car.release_year}</b></p>'

        drop_items.append(item)
        swal_items.append(swal_item)
        drop_items_info.update({car.pk: model_to_dict(car)})
    result = {'cars': drop_items, 'cars_info': drop_items_info, 'swal_items': swal_items}

    return result


class IndexView(TemplateView):
    template_name = 'core/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hi'] = 'Hello Cars!!!'

        all_cars = Car.objects.all()

        data = prepare_car_info(all_cars)

        context['cars'] = json.dumps(data['cars'])
        context['cars_info'] = json.dumps(data['cars_info'])
        context['swal_items'] = json.dumps(data['swal_items'])

        return context


class AddCarView(View):

    def get(self, request, *args, **kwargs):

        if not request.is_ajax():
            return HttpResponse('ajax request only on this url')
        else:
            model = request.GET.get('model', None)
            if model:
                management.call_command('create_test_car', count=1, model=model)
            else:
                management.call_command('create_test_car', count=1)

            last_car = Car.objects.latest()
            added_car = prepare_car_info([last_car])

            return JsonResponse(added_car)


class DelAllCarView(View):

    def post(self, request, *args, **kwargs):
        exter, del_exter = ExteriorGallery.objects.all().delete()
        inter, del_inter = InteriorGallery.objects.all().delete()
        car, del_car = Car.objects.all().delete()

        result = {'exterior': (exter, del_exter,),
                  'interior': (inter, del_inter,),
                  'cars': (car, del_car,),
                  }

        return JsonResponse(result)


class EditGarageView(View):

    modal_template = 'core/uni_table.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        car_table = render_to_string(self.modal_template, context=context)
        return JsonResponse({'car_table': car_table})

    def get_context(self):

        cars = Car.objects.all()
        table_headers = [
            'model',
            'release',
            'color',
            'trank',
            'engine',
            'transmission',
            'rate',
            'isrent',
            'owner'
        ]
        table_data = []
        for c in cars:
            table_data.append(
                [
                    c.params['model'],
                    c.release_year,
                    get_color_car_icon(c.params["color"]),
                    c.params["trank_vol"],
                    c.params["engine_vol"],
                    c.params["transmission"],
                    c.base_rate,
                    str(c.give_to_rent),
                    c.owner.username
                ]
            )
        context = {
            'table_headers': table_headers,
            'table_data': table_data
        }

        return context


class fifteen(TemplateView):

    template_name = 'edu/fift.html'

