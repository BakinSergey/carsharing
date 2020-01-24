from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db.models import DurationField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import datetime
from django.utils import timezone

from os import path
from functools import partial
from core import utils


# имя(задается на двух языках en, ru, реализацию сделать с учетом возможного увеличения языков),
# реализовано так:
# при добавлении новой марки или бренда машины, в сериалайзере создаются обязательные для заполнения текст.поля
# для всех имеющихся на данный момент в системе языков.
# в случае если запрашивается модель/бренд на языке, для которого нет перевода, то в модель бренда/модели записывается значение
# 'lang_acronim': 'not translated', так в последствии можно сделать вьюху для технического персонала сайта - переводить все модели/бренды к-е 'not translated'


# email, name, lang
class csUser(AbstractUser):
    class Meta:
        verbose_name = _(u'Пользователь')
        verbose_name_plural = _('Пользователи')

    # язык пользователя, собтвенника авто -
    # на основании этого языка для конечного пользователя будет рассчитываться цена аренды
    # например:
    # В Москве сдает свою машину в аренду немец, выбирает DE локаль, вводит base_rate в дойч-марках(ему так понятно "за сколько")
    # Арендует эту машину чукча, устанавливает CHU-котский локаль, и видит цену за аренду в час в чукостских     тугриках(ему тоже так понятно "за сколько")
    # При этом и тот и другой видят сайт на своем родном языке.

    lang = models.CharField(verbose_name=_(u'Язык интерфейса'), choices=settings.LANGUAGES, max_length=10,
                            default=settings.LANGUAGE_CODE)

    user_info = JSONField(default=dict, blank=True)

    avatar = models.ImageField(max_length=127, null=True, blank=True, verbose_name='Фото профиля',
                               upload_to=path.join('user', 'logo'), default='./user/logo/default.png')

    def get_roles(self):
        return [g.name for g in self.groups.all()]


# PS - в процессе решил что Бренд Модель и Модификация(тех параметры) будут xml(или json) - справочником,
# а не моделями в БД(снизить число запросов к БД)

# # Бренд машины
# class CarBrand(models.Model):
#     class Meta:
#         verbose_name = _(u'Бренд')
#         verbose_name_plural = _('Бренды')
#
#     car_brand_tr = JSONField(default=dict, blank=False)
#     current_logo = models.ImageField(max_length=127, verbose_name='Текущий логотип бренда',
#                                      upload_to=path.join('car', 'brand'))
#
#
# # Модель машины
# class CarModel(models.Model):
#     class Meta:
#         verbose_name = _(u'Модель')
#         verbose_name_plural = _('Модели')
#
#     model_name = models.CharField(verbose_name=_(u'Марка машины'), max_length=30, blank=False)
#     car_model_tr = JSONField(default=dict, blank=False)
#
#     brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, blank=False, related_name='models')
#     pass
#
#
# # Модификация - Лада Гранта Норма 1.6 AT // Acura MDX 3.5 V6  // etc
# class CarModificaion(models.Model):
#     class Meta:
#         verbose_name = _(u'Модификация')
#         verbose_name_plural = _('Модификации')
#
#     model_name = models.CharField(verbose_name=_(u'Марка машины'), max_length=30, blank=False)


# Машина(связываемая с пользователем сущность - ^rent entity^)
class Car(models.Model):
    class Meta:
        verbose_name = _(u'Авто')
        verbose_name_plural = _(u'Авто')
        get_latest_by = 'append_date'

    year_choices = [(r, r) for r in range(1984, datetime.now().year + 1)]
    current_year = datetime.now().year

    release_year = models.IntegerField(verbose_name=_(u'Год выпуска'), choices=year_choices, default=current_year)

    append_date = models.DateTimeField(verbose_name=_(u'Дата добавления'), auto_now_add=True, db_index=True,
                                       blank=False)

    is_single_color = models.BooleanField(verbose_name=_(u'Заводская окраска?'), default=True)
    with_graffity = models.BooleanField(verbose_name=_(u'Граффити?'), default=False)
    is_pumped = models.BooleanField(verbose_name=_(u'Прокачана?'), default=False)

    params = JSONField(verbose_name=_(u'Характеристики'), default=dict, blank=True)
    desc = models.CharField(verbose_name=_(u'Дополнительное описание'), max_length=120, blank=False)

    base_rate = models.FloatField(verbose_name=_(u'Базовая цена аренды, за 1 час'),
                                  validators=(MinValueValidator(0),), blank=False)

    give_to_rent = models.BooleanField(verbose_name=_(u'Сдавать в аренду ?'), default=False)

    owner = models.ForeignKey(csUser, verbose_name=_(u'Собственник'), on_delete=models.CASCADE, db_index=True,
                              related_name='cars')

    def __str__(self):
        return f'{self.params["model"]} |--| {self.params["color"]}'


class ExteriorGallery(models.Model):
    image = models.ImageField(max_length=127, verbose_name='Фото авто(экстерьер)',
                              upload_to=path.join('car', 'exterior'), default='./car/exterior/default.png')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='exterior_images')

    # ref for right media dir
    add_sample_image = partial(utils.get_n_photo_by_theme, category='car/exterior')


class InteriorGallery(models.Model):
    image = models.ImageField(max_length=127, verbose_name='Фото авто(интерьер)',
                              upload_to=path.join('car', 'interior'), default='./car/interior/default.png')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='interior_images')

    # ref for right media dir
    add_sample_image = partial(utils.get_n_photo_by_theme, category='car/interior')


class RentEntry(models.Model):
    user = models.ForeignKey(csUser, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start = models.DateTimeField()
    duration = DurationField(verbose_name=_(u'Продолжительность аренды', ))
