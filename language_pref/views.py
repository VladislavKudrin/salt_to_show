from django.shortcuts import render
from django.utils.http import is_safe_url, urlunquote
from django import http
from django.utils.translation import (
    LANGUAGE_SESSION_KEY, check_for_language, get_language, to_locale,
)
from django.urls import translate_url

from accounts.models import LanguagePreference

DEFAULT_PACKAGES = ['django.conf']
LANGUAGE_QUERY_PARAMETER = 'language'



def set_language(request):
    next = request.POST.get('next', request.GET.get('next'))
    if ((next or not request.is_ajax()) and
            not is_safe_url(url=next, allowed_hosts={request.get_host()}, require_https=request.is_secure())):
        next = request.META.get('HTTP_REFERER')
        if next:
            next = urlunquote(next)  # HTTP_REFERER may be encoded.
        if not is_safe_url(url=next, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
            next = '/'
    response = http.HttpResponseRedirect(next) if next else http.HttpResponse(status=204)
    if request.method == 'POST':
        lang_code = request.POST.get(LANGUAGE_QUERY_PARAMETER)
        if lang_code and check_for_language(lang_code):
            if next:
                next_trans = translate_url(next, lang_code)
                if next_trans != next:
                    response = http.HttpResponseRedirect(next_trans)
            if hasattr(request, 'session'):
                request.session[LANGUAGE_SESSION_KEY] = lang_code
            else:
                response.set_cookie(
                    settings.LANGUAGE_COOKIE_NAME, lang_code,
                    max_age=settings.LANGUAGE_COOKIE_AGE,
                    path=settings.LANGUAGE_COOKIE_PATH,
                    domain=settings.LANGUAGE_COOKIE_DOMAIN,
                )
            if request.user.is_authenticated():
                user = request.user
                qs_lang = LanguagePreference.objects.filter(user=user)
                if qs_lang.exists():
                    LanguagePreference.objects.update(user=user, language=lang_code)
                else:
                    LanguagePreference.objects.create(user=user, language=lang_code)
    return response



