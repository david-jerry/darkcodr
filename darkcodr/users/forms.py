import datetime
import re
from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm, ResetPasswordKeyForm, ChangePasswordForm, AddEmailForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms

from countries_plus.models import Country

from .models import Profile, CardDetail

User = get_user_model()


# custom credit card fields
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

class CreditCardNumberField(forms.CharField):
    """ A newforms field for a creditcard number """
    def clean(self, value):

        numbers = forms.CharField.clean(self, value)
        number = StripToNumbers(numbers)
        if not ValidateLuhnChecksum(number) or not number.isdigit() or len(number) < 13 or len(number) > 19 or not re.match('[^4[0-9]{12}(?:[0-9]{3})?$]', number) or not re.match('[^5[1-5][0-9]{14}|^(222[1-9]|22[3-9]\\d|2[3-6]\\d{2}|27[0-1]\\d|2720)[0-9]{12}$]', number) or not re.match('[^3[47][0-9]{13}$]', number):
            raise forms.ValidationError('Not a valid credit card number.')

        return number


class CreditCardExpiryMonth(forms.CharField):
    """ A new forms field for a creditcard expiry month """
    def clean(self, value):
        number = forms.CharField.clean(self, value.strip())

        # Just check MM/YY Pattern
        r = re.compile('^([0-9][0-9])$')
        m = r.match(number)
        if m == None:
            raise forms.ValidationError('Must be in the format MM. i.e. "11" for Nov.')

        # Check that the month is 1-12
        month = int(m.groups()[0])
        if month < 1 or month > 12:
            raise forms.ValidationError('Month must be in the range 1 - 12.')

        return number

class CreditCardExpiryYear(forms.CharField):
    """ A new forms field for a creditcard expiry year"""
    def clean(self, value):
        number = forms.CharField.clean(self, value.strip())

        # Just check MM/YY Pattern
        r = re.compile('^([0-9][0-9])$')
        m = r.match(number)
        if m == None:
            raise forms.ValidationError('Must be in the format YY. i.e. "23" for 2023.')

        # Check that the year is not far into the future
        year = int(m.groups()[0])
        curr_year = datetime.datetime.now().year % 100
        max_year = curr_year + 10
        if year > max_year or year < curr_year:
            raise forms.ValidationError('Year must be in the range %s - %s.' % (str(curr_year).zfill(2), str(max_year).zfill(2),))

        return number


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """
    name = forms.CharField(max_length=255, required=True)
    country_of_origin = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label=_("Select Country"), widget=forms.Select(attrs={'title':'Country of Origin', 'placeholder':_('Country of Origin'),}))

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        # Field labels
        self.fields['email'].label = ""
        self.fields['name'].label = ""
        self.fields['username'].label = ""
        self.fields['country_of_origin'].label = ""
        self.fields['password1'].label = ""
        self.fields['password2'].label = ""
        self.fields['terms'].label = ""

        # widget
        self.fields['email'].widget = forms.EmailInput(attrs={'title':'Email Address', 'placeholder':_('Email Address'),})
        self.fields['name'].widget = forms.TextInput(attrs={'title':'Your Name/Company Representative', 'placeholder':_('Your Name/Company Name'),})
        self.fields['username'].widget = forms.TextInput(attrs={'title':'Username', 'placeholder':_('Username'),})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'title':'Password', 'placeholder':_('Password'),})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'title':'Confirm Password', 'placeholder':_('Confirm Password'),})
        self.fields['terms'].widget = forms.CheckboxInput(attrs={'title':'Accept Terms', 'placeholder':_('Accept Terms'),})

    def save(self, request):
        user = super(UserSignupForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.save()
        return user


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """

class UserCardForm(forms.ModelForm):
    card_type = forms.ChoiceField(choices=CardDetail.CARD_TYPE, widget=forms.Select(attrs={'title':'Card Type', 'placeholder':_('Card Type'),}))
    card_number = CreditCardNumberField(label="", required=True)
    card_expiry_month = CreditCardExpiryMonth(label="", required=True)
    card_expiry_year = CreditCardExpiryYear(label="", required=True)

    class Meta:
        model = CardDetail
        fields = ['card_type', 'card_number', 'card_cvv', 'card_expiry_month', 'card_expiry_year']
        widgets = {
            'card_number': forms.NumberInput(attrs={'title':'Card Number', 'placeholder':_('0000 0000 0000 0000'),}),
            'card_cvv': forms.NumberInput(attrs={'title':'CVV', 'placeholder':_('CVV'),}),
            'expiry_month': forms.NumberInput(attrs={'title':'Expiry Month', 'placeholder':_('00'),}),
            'expiry_year': forms.NumberInput(attrs={'title':'Expiry Year', 'placeholder':_('00'),}),
        }

class UserProfileUpdateForm(forms.ModelForm):
    """User profile fields that can be updated

    Args:
        forms (_type_): _description_
    """
    name = forms.CharField(max_length=255, required=True)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label=_("Select Country"), widget=forms.Select(attrs={'title':'Country of Headquaters', 'placeholder':_('Country of Headquaters'),}))

    class Meta:
        model = Profile
        fields = [
            'name',
            'phone',
            'office_phone',
            'office_address',
            'city',
            'state',
            'country',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = ""
        self.fields['phone'].label = ""
        self.fields['office_phone'].label = ""
        self.fields['office_address'].label = ""
        self.fields['city'].label = ""
        self.fields['state'].label = ""
        self.fields['postcode'].label = ""

        self.fields['name'].widget = forms.TextInput(attrs={'title':'Your Company Name', 'placeholder':_('Your Company Name'),})
        self.fields['phone'].widget = forms.NumberInput(attrs={'Type':'tel', 'title':'Phone Number', 'placeholder':_('Phone Number'),})
        self.fields['office_phone'].widget = forms.NumberInput(attrs={'Type':'tel', 'title':'Office Phone Number', 'placeholder':_('Office Phone Number'),})
        self.fields['office_address'].widget = forms.TextInput(attrs={'id':'office_address', 'title':'Office Address', 'placeholder':_('Office Address'),})
        self.fields['city'].widget = forms.TextInput(attrs={'id':'city', 'title':'City', 'placeholder':_('City'),})
        self.fields['state'].widget = forms.TextInput(attrs={'id':'state', 'title':'State/Province', 'placeholder':_('City'),})
        self.fields['postcode'].widget = forms.TextInput(attrs={'id':'postcode', 'title':'Postal Code', 'placeholder':_('Postal Code'),})


class UserLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = ""
        self.fields['password'].label = ""

        self.fields['login'].widget = forms.TextInput(
            attrs={'type': 'email', 'class': 'textinput textInput form-control fbc-has-badge fbc-UID_1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-dark rounded-t-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-xl'})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': 'textinput textInput form-control fbc-has-badge fbc-UID_1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-dark rounded-b-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-xl'})

class ResetUserPassword(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(ResetUserPassword, self).__init__(*args, **kwargs)
        self.fields['email'].label = ""
        self.fields['email'].widget = forms.EmailInput(
            attrs={'placeholder':'Email Address', 'class': 'textinput textInput form-control fbc-has-badge fbc-UID_1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-dark rounded-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-xl'})






# way to do a model form select field
# secretdocs = forms.ChoiceField(choices=[(doc.uid, doc.name) for doc in Document.objects.all()])
