import datetime

from decimal import Decimal
from django.utils import translation

from django.db.models import Sum

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render

from django.conf import settings
from django.contrib import messages
from django.template.loader import get_template, render_to_string
from django.utils.safestring import mark_safe

from django.views.generic import DetailView, RedirectView, UpdateView, CreateView

from darkcodr.utils.logger import LOGGER

def switch_language(request, **kwargs):
    language = kwargs.get('language')
    redirect_url_name = request.GET.get('url') # e.g. '/about/'

    # make sure language is available
    valid = False
    for l in settings.LANGUAGES:
        if l[0] == language:
            valid = True
    if not valid:
        raise Http404(_('The selected language is unavailable!'))

    # Make language the setting for the session
    translation.activate(language)
    # response = redirect(reverse(redirect_url_name)) # Changing this to use reverse works

    # response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    # return response
    return redirect(reverse(language, kwargs={'url':redirect_url_name})) # Changing this to use reverse works

