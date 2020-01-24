"""carsharing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.decorators.cache import never_cache
from django.contrib.staticfiles.views import serve

from core.views import IndexView, AddCarView, DelAllCarView, EditGarageView,fifteen

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('add_car/', AddCarView.as_view(), name="ajax_add_car"),
    path('del_all_car/', DelAllCarView.as_view(), name="ajax_del_car"),
    path('edit_garage/', EditGarageView.as_view(), name="edit_garage"),
    path('15/', fifteen.as_view(), name="fif"),
]


if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns.append(path('static/<path:path>', never_cache(serve)))
