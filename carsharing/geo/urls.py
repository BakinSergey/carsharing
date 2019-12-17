from .views import *

from django.urls import path

urlpatterns = [
    path('', TestModelView.as_view(), name="testmodel"),
]


