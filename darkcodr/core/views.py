import datetime

from decimal import Decimal
from urllib import response
from django.utils import translation

from django.db.models import Sum
from django.conf import settings
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


from push_notifications.api.rest_framework import WebPushDeviceViewSet
from push_notifications.models import WebPushDevice
from rest_framework.decorators import api_view
from django.views.decorators.http import require_http_methods

from django.templatetags.static import static

@require_http_methods(['GET'])
def service_worker(request):
    sw_path = "sw.js"
    context = {
        "home_url": reverse('home'),
        "about_url": reverse('about'),
        "service_url": reverse('services'),
        "offline_url": reverse('offline'),
        "logo_url": static("assets/android-chrome-512x512.png"),
        "home_revision": 123456,
        "about_revision": 123456,
        "service_revision": 123456,
        "offline_revision": 123456
    }
    return render(request, sw_path, content_type="application/javascript", context=context)

def manifest(request):
    sw_path = "manifest.json"
    context = {
        "home_url": reverse('home'),
        "36x36": static("assets/android-chrome-36x36.png"),
        "48x48": static("assets/android-chrome-48x48.png"),
        "72x72": static("assets/android-chrome-72x72.png"),
        "96x96": static("assets/android-chrome-96x96.png"),
        "144x144": static("assets/android-chrome-144x144.png"),
        "192x192": static("assets/android-chrome-192x192.png"),
        "256x256": static("assets/android-chrome-256x256.png"),
        "384x384": static("assets/android-chrome-384x384.png"),
        "512x512": static("assets/android-chrome-512x512.png")
    }
    return render(request, sw_path, content_type="application/javascript", context=context)

class AnonymousWebPushDeviceViewSet(WebPushDeviceViewSet):
    def perform_create(self, serializer):
        # if not is_authenticated, can still work
        serializer.save()
        return super().perform_create(serializer)


@api_view(["POST"])
# @require_http_methods(['POST'])
def send_notification(request):
    registration_id = request.data.get('registration_id')
    if registration_id:
        device = WebPushDevice.objects.get(registration_id=registration_id)
        if device:
            device.send_message('Hello World')
    return HttpResponse()

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
