import json
import sys, os
import subprocess

from collections import defaultdict
from datetime import timedelta

from core.models import Car, csUser, ExteriorGallery, InteriorGallery
from django.conf import settings

from django.core.management.base import BaseCommand
from django.contrib.auth import models
from django.core.management import call_command
from random import choice, choices

from random import randrange

# call_command('my_command', 'foo', bar='baz')
from django.db.models.functions import datetime
from django.utils import timezone, duration
from django.utils.translation import ugettext_lazy as _


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--model',
            dest='model',
            default=None,
            type=str,
            help='make car specified model',
        )
        parser.add_argument(
            '--count',
            dest='count',
            default=None,
            type=int,
            help='make N car',
        )

    base_colors = (
        _(u'красный'), _(u'оранжевый'), _(u'желтый'), _(u'знать'), _(u'голубой'), _(u'синий'), _(u'фиолтетовый'),)

    vaz_colors = (_('Белый "Ледниковый" (221)'), _('Оранжевый "Марс" (130)'), _('Красный "Сердолик" (195)'),
                  _('Коричневый "Ангкор" (246)'), _('Серо-бежевый "Карфаген" (247) '), _('Ярко-синий "Дайвинг" (476)'),
                  _('Серо-голубой "Фантом" (496)'), _('Серый "Плутон" (608)'), _('Черный "Маэстро" (653) '),
                  _('Серебристый "Платина" (691)'))

    car_models = (
        _(u'Лада Гранта'), _(u'Лада Приора'), _(u'Touareg'), _(u'Toyota Prado'),
        _(u'Авто Москвич'), _(u'Запорожец'), _(u'Лада Веста'), _(u'УАЗ 469'),
        _(u'Волга Siber'), _(u'Porcshe Cayenne'), _(u'Porcshe Panamera')
    )

    @staticmethod
    def random_date():
        """
        This function will return a random datetime between two datetime
        objects.
        """
        d1 = datetime.datetime(1984, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        d2 = datetime.datetime.now(tz=timezone.utc)

        delta = d2 - d1
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return d1 + timedelta(seconds=random_second)

    def generate_car_params(self, carmodel):

        group = models.Group.objects.get(name='holder')
        holders = group.user_set.all()

        self.car['params'] = {}
        self.car['params'].update(
            {
             'model': str(carmodel),
             'color': str(choice(self.base_colors + self.vaz_colors)),
             'engine_vol': choices(
                 population=(0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.6, 1.8, 2.0, 2.4, 2.6, 3.0),
                 weights=(0.1, 0.1, 0.1, 0.1, 0.2, 0.4, 0.6, 0.4, 0.2, 0.1, 0.1, 0.1),
                 k=1)[0],
             'transmission': choice(('5x', '6x',)),
             'trank_vol': choice(('400L', '500L', '600L', '700L', '800L',))}
        )

        self.car.update({
            'is_single_color': choice((True, False,)),
            'with_graffity': choice((True, False,)),
            'is_pumped': choice((True, False,)),
            'give_to_rent': choices(population=(True, False,), weights=(0.75, 0.25), k=1)[0],
            'release_year': choice(range(1984, 2019)),
            'append_date': self.random_date(),
            'base_rate': 100 if self.car['params']['engine_vol'] < 1.6 else 200,
            'desc': str(_('описание машины')),

            'owner_id': choice(holders).pk,
        })


    def handle(self, **options):
        cars = []

        carcount = options['count'] or 1

        for c in range(carcount):
            self.car = {}
            carmodel = choice(self.car_models) if not options.get('model') else options.get('model')
            self.generate_car_params(carmodel)

            new_car = Car.objects.create(**self.car)
            print(self.car)

            exterior_images = ExteriorGallery.add_sample_image(1, carmodel, (320, 240))
            interior_images = InteriorGallery.add_sample_image(1, carmodel + 'салон', (320, 240))

            for ei in exterior_images:
                ExteriorGallery.objects.create(image=ei, car=new_car)

            for ii in interior_images:
                InteriorGallery.objects.create(image=ii, car=new_car)

            print(f'car: id={new_car.pk} created')

            cars.append(new_car.pk)


