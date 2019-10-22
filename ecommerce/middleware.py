from django.utils import translation
from django.conf import settings

from accounts.models import LanguagePreference

class LanguagePreferenceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        language_pref = settings.LANGUAGE_CODE
        if request.user.is_authenticated():
            user = request.user
            qs_lang = LanguagePreference.objects.filter(user=user)
            if qs_lang.exists():
                language_pref = qs_lang.first().language
            if hasattr(request, 'session'):
                request.session[translation.LANGUAGE_SESSION_KEY] = language_pref
        if not request.session.get(translation.LANGUAGE_SESSION_KEY):
            translation.activate(language_pref)
        

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response