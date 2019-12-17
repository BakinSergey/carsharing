from django.utils.translation import activate


def language_activator(get_responce):

    def middleware(request):
        lang = request.GET.get('lang', 'ru')
        activate(lang)

        request.lang = lang

        return get_responce(request)

    return middleware
