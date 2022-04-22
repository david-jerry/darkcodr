import datetime

from decimal import Decimal
import re

from django.db.models import Sum

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from django.conf import settings
from django.contrib import messages
from django.template.loader import get_template, render_to_string
from django.utils.safestring import mark_safe

from django.views.generic import DetailView, RedirectView, UpdateView, CreateView

from darkcodr.utils.logger import LOGGER
from darkcodr.utils.emails import plain_email, support_email, pdf_attachment_email
from darkcodr.utils.unique_generators import unique_id_generator

from .models import Profile, CardDetail
from .forms import UserProfileUpdateForm

User = get_user_model()

"""
    Provides functions & Fields for validating credit card numbers
    Thanks to David Shaw for the Luhn Checksum code
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/172845)
"""




def ValidateLuhnChecksum(number_as_string):
    """ checks to make sure that the card passes a luhn mod-10 checksum """

    checksum = 0
    num_digits = len(number_as_string)
    oddeven = num_digits & 1

    for i in range(0, num_digits):
        digit = int(number_as_string[i])

        if not (( i & 1 ) ^ oddeven ):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9

        checksum = checksum + digit

    return ( (checksum % 10) == 0 )

def ValidateCharacters(number):
    """ Checks to make sure string only contains valid characters """
    return re.compile('^[0-9 ]*$').match(number) != None

def StripToNumbers(number):
    """ remove spaces from the number """
    if ValidateCharacters(number):
        result = ''
        rx = re.compile('^[0-9]$')
        for d in number:
            if rx.match(d):
                result += d
        return result
    else:
        raise Exception('Number has invalid digits')


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


@login_required
def user_update_view(request, username):
    name = request.POST.get('name')

    user = User.objects.get(username=username)

    user.name = name
    user.save()

    messages.success(request, "Updated Personal Information Successfully!")
    return redirect(reverse("users:detail", kwargs={"username": user.username}))


@login_required
def user_update_company_view(request, username):
    company_name = request.POST.get('company_name')
    phone = request.POST.get('phone')
    office_phone = request.POST.get('office_phone')
    office_address = request.POST.get('office_address')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip_code = request.POST.get('postcode')

    user = User.objects.get(username=username)

    Profile.objects.filter(user=user).update(name=company_name, phone=phone, office_phone=office_phone, office_address=office_address, city=city, state=state, zip_code=zip_code)

    messages.success(request, "Updated Company Information Successfully!")
    return redirect(reverse("users:detail", kwargs={"username": user.username}))


@login_required
def user_add_card(request, username):
    user = User.objects.get(username=username)
    card_type = request.POST.get('card_type')
    card_number = request.POST.get('card_number')
    card_expiry_month = request.POST.get('card_expiry_month')
    card_expiry_year = request.POST.get('card_expiry_year')
    card_cvv = request.POST.get('card_cvv')
    saved_card = request.POST.get('saved_card')

    number = StripToNumbers(card_number)

    # TODO: Add auto fill for card_type with javascript

    if saved_card == "on" and card_number is not None or card_number != "" or ValidateLuhnChecksum(number) != False:
        CardDetail.objects.filter(user=user, saved_card=True).update(saved_card=False)
        CardDetail.objects.create(user=user, card_type=card_type, card_number=number, card_expiry_month=card_expiry_month, card_expiry_year=card_expiry_year, card_cvv=card_cvv, saved_card=True)
        messages.success(request, "Updated and Saved Card Information Successfully!")
    elif saved_card == "off" and card_number is None or card_number == "" or ValidateLuhnChecksum(number) != False:
        CardDetail.objects.create(user=user, card_type=card_type, card_number=number, card_expiry_month=card_expiry_month, card_expiry_year=card_expiry_year, card_cvv=card_cvv, saved_card=False)
        messages.success(request, "Saved New Card Information Successfully!")
    return redirect(reverse("users:detail", kwargs={"username": user.username}))




class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()





























# HTMX Form validations

def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("This username already exists")
    else:
        return HttpResponse("")

def check_email(request):
    email = request.POST.get('email')
    if get_user_model().objects.filter(email=email).exists():
        return HttpResponse("This email already exists")
    else:
        return HttpResponse("")

def check_password(request):
    username = request.POST.get('username')
    name = request.POST.get('name')
    password = request.POST.get('password1') or request.POST.get('password')
    password2 = request.POST.get('password2')
    if len(password) < 6:
        return HttpResponse("This password is too short")
    elif re.search('[0-9]',password) is None:
        return HttpResponse("This password must contain at least one number")
    elif re.search('[A-Z]',password) is None:
        return HttpResponse("This password must contain at least one capital letter")
    elif password == username or password == name:
        return HttpResponse("This password is too similar to your username or name")
    elif password2 != password:
        return HttpResponse("The passwords do not match")
    else:
        return HttpResponse("")

def check_card(request):
    card_number = request.POST.get('card_number')
    card_expiry_month = request.POST.get('card_expiry_month')
    card_expiry_year = request.POST.get('card_expiry_year')

    if CardDetail.objects.filter(card_number=card_number).exists():
        return HttpResponse("{user} already used this card".format(user=CardDetail.objects.get(card_number=card_number).user.username.title()))
    elif re.search('[^5[1-5][0-9]{14}|^(222[1-9]|22[3-9]\\d|2[3-6]\\d{2}|27[0-1]\\d|2720)[0-9]{12}$]',card_number) is None:
        card_type = "MasterCard"
        return card_type
    elif re.search('[^4[0-9]{12}(?:[0-9]{3})?$]',card_number) is None:
        card_type = "Visa"
        return card_type
    elif re.search('[^3[47][0-9]{13}$]',card_number) is None:
        card_type = "American Express"
        return card_type
    elif card_number != re.search('[^4[0-9]{12}(?:[0-9]{3})?$]',card_number).group(0) or card_number != re.search('[^5[1-5][0-9]{14}|^(222[1-9]|22[3-9]\\d|2[3-6]\\d{2}|27[0-1]\\d|2720)[0-9]{12}$]',card_number).group(0) or card_number != re.search('[^3[47][0-9]{13}$]',card_number).group(0) or ValidateLuhnChecksum(number) == False:
        return HttpResponse("Invalid card number")
    elif len(card_expiry_month) != 2 or len(card_expiry_year) != 2 or card_expiry_month == "00" or card_expiry_year == "00":
        return HttpResponse("Invalid card expiry date")
    elif card_expiry_month < 1 or card_expiry_month > 12:
        return HttpResponse("Invalid card expiry month")
    elif card_expiry_year < datetime.datetime.now().year % 100 or card_expiry_year > datetime.datetime.now().year % 100 + 10:
        return HttpResponse("Invalid card expiry year")
    else:
        return HttpResponse("")

