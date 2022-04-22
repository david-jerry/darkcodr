import uuid
import datetime
import re
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    DO_NOTHING,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    FileField,
    ForeignKey,
    ManyToManyField,
    ImageField,
    IntegerField,
    OneToOneField,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    UUIDField,
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django import forms

from stdimage import StdImageField
from model_utils.models import TimeStampedModel
from countries_plus.models import Country
from django.utils.timezone import now

def three_months():
    return datetime.datetime.now() + datetime.timedelta(days=90)

def two_weeks():
    return datetime.datetime.now() + datetime.timedelta(days=14)

def one_week():
    return datetime.datetime.now() + datetime.timedelta(days=7)


class User(AbstractUser):
    """
    Default custom user model for darkcodr.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """
    #: User's referral code
    unique_id = CharField(max_length=50, editable=True, blank=True, unique=True)

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Your Name/Company Representative"), blank=True, max_length=255)


    subscribe_newsletter = BooleanField(default=False)
    accept_terms = BooleanField(default=False)
    # once a first purchase occurs the referrer gets 3 dark credits
    first_purchase = BooleanField(default=True)
    points = PositiveIntegerField(default=0)

    #: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
    country_of_origin = ForeignKey(Country, on_delete=DO_NOTHING, default="NG", blank=True, null=True)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_recommended_profiles(self):
        qs = User.objects.all()
        # empty recommended lists
        my_recs = []
        for user in qs:
            if user.recommended_by == self:
                my_recs.append(user)
        return my_recs

    def get_recommended_count(self):
        qs = User.objects.all()
        # empty recommended lists
        my_recs = []
        for user in qs:
            if user.recommended_by == self:
                my_recs.append(user)
        return len(my_recs) or 0

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    class Meta:
        managed = True
        verbose_name = "User Account"
        verbose_name_plural = "User Accounts"
        ordering = ["-date_joined"]


class CardDetail(TimeStampedModel):
    MASTER_CARD = "MasterCard"
    VISA = "Visa"
    AMEX = "American Express"
    CARD_TYPE = (
        (MASTER_CARD, "MasterCard"),
        (VISA, "Visa"),
        (AMEX, "American Express"),
    )
    user = ForeignKey(User, on_delete=CASCADE, related_name=_("card_detail"))
    card_type = CharField(max_length=50, blank=True, null=True, choices=CARD_TYPE)
    card_number = CharField(max_length=16, blank=True, null=True)
    card_expiry_month = PositiveIntegerField(blank=True, null=True)
    card_expiry_year = PositiveIntegerField(blank=True, null=True)
    card_cvv = PositiveIntegerField(blank=True, null=True)
    saved_card = BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s card details"

    class Meta:
        verbose_name = "Card Details"
        verbose_name_plural = "Card Details"
        ordering = ["-created"]


class Profile(TimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name=_("profile"))

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of Company"), blank=True, max_length=500)
    phone = CharField(_("Mobile Number"), unique=True, max_length=11, blank=True, null=True, help_text=_("eg: 07076879898"))
    office_phone = CharField(_("Office Number"), unique=True, max_length=11, blank=True, null=True, help_text=_("eg: 07076879898"))

    #: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
    office_address = CharField(_("Business Address"), max_length=255, blank=True, null=True)
    city = CharField(_("City"), max_length=255, blank=True, null=True)
    state = CharField(_("State/Province"), max_length=255, blank=True, null=True)
    postcode = CharField(_("Postal Code"), max_length=10, blank=True, null=True)
    country = ForeignKey(Country, on_delete=DO_NOTHING, blank=True, null=True)


    def __str__(self):
        return f"{self.user.username}'s profile"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ["-created"]







