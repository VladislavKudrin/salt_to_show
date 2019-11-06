from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.urlresolvers import reverse
import re
from django.utils.translation import gettext as _ 
from django.utils.translation import pgettext
User = get_user_model()

from marketing.models import MarketingPreference
from .models import EmailActivation, GuestEmail, LanguagePreference, Region
from .signals import user_logged_in_signal
from django.core.validators import RegexValidator
from marketing.utils import Mailchimp

class ReactivateEmailForm(forms.Form):
    error_css_class = 'error'
    email = forms.EmailField()
    def __init__(self, request, *args, **kwargs):
        super(ReactivateEmailForm, self).__init__(*args, **kwargs)
        self.request=request
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_objects = EmailActivation.objects.email_exists(email)
        if not user_objects.exists():
            reset_link = reverse("login")
            msg = _("""This email does not exist or already acivated. Would you like to <a href="{link}">register</a>?""").format(link=reset_link)
            raise forms.ValidationError(mark_safe(msg))
        return email

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email',)
    # def clean_password2(self):
    #     # Check that the two password entries match
    #     # password1 = self.cleaned_data.get("password1")
    #     # password2 = self.cleaned_data.get("password2")
    #     # if password1 and password2 and password1 != password2:
    #     #     raise forms.ValidationError("Passwords don't match")
    #     return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserDetailChangeForm(forms.ModelForm): 
    username  = forms.CharField(required=True, widget=forms.TextInput(attrs={"class":'form-control'}))
    region = forms.ChoiceField(widget=forms.Select(), required=False)
    full_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":'form-control', 'disabled':'true'}), required=False)
    subscribed = forms.BooleanField(required=False)
    profile_foto = forms.FileField(required=False, widget=forms.FileInput(attrs={'class':'avatar-upload-button','id':'avatar_custom'} ))
    class Meta:
        model = User
        fields = [
                'username',
                'region',
                'full_name',
                'profile_foto',
                    ]
    def __init__(self, request, *args, **kwargs):
        super(UserDetailChangeForm, self).__init__(*args, **kwargs)
        alphanumeric = RegexValidator(r'^[0-9a-zA-Z_.-]+$', _('Only alphanumeric characters are allowed'))
        self.fields['username'].label = _('Username')
        self.fields['username'].widget.attrs['placeholder'] = _('Your username')
        self.fields['username'].validators = [alphanumeric]
        self.fields['region'].label = _('Region')
        self.fields['full_name'].label = _('Name')
        self.fields['full_name'].widget.attrs['placeholder'] = _('Your full name')
        self.fields['full_name'].widget.help_text = _('Cannot change email')
        self.fields['subscribed'].label = _('Recieve marketing email?')
        self.fields['profile_foto'].label = _('Profile photo')
        self.fields['profile_foto'].widget.attrs['label_for_btn'] = pgettext('profile_update','Update')
        #REGIONS
        self.initial['region'] = request.user.region
        if self.initial['region'] is None: 
            self.initial['region'] = ('default', _('-- Please select your region --'))
        region_choices = [(e.region, e.region) for e in Region.objects.all()] #currently available options
        region_choices.append(tuple(('default', _('-- Please select your region --')))) #append default value
        self.fields['region'].choices = region_choices

        self.request = request
        self.fields['email'].initial=request.user.email
        self.fields['subscribed'].initial=request.user.marketing.subscribed
        self.fields['subscribed'].widget.attrs['class']='custom-checkbox'

    # def clean_username(self):
    #     data = self.cleaned_data['username']
    #     contains_rus = bool(re.search('[а-яА-Я]', data))
    #     if contains_rus:
    #         raise forms.ValidationError("Юзернейм должен содержать только латинские символы")
    #     return data

    def clean_subscribed(self):
        marketing_pref = MarketingPreference.objects.filter(user=self.request.user)
        subscribed_user = self.cleaned_data.get('subscribed')
        marketing_pref.update(subscribed=subscribed_user)
        marketing_pref.first().save()

    def clean_region(self):
        data = self.cleaned_data['region']
        if data == 'default':
            raise forms.ValidationError(_("You must select a region"))
        clean_data = Region.objects.filter(region=data)[0]
        # user = self.request.user
        # mark_pref = MarketingPreference.objects.filter(user=user).first()
        # if mark_pref.subscribed == True: 
        #     print('Forms Acc, if True')
        #     response_status, response = Mailchimp().change_subscription_status(user.email, 'subscribed')
        # elif mark_pref.subscribed == False:
        #     print('Forms acc, if True') 
        #     response_status, response = Mailchimp().change_subscription_status(user.email, 'unsubscribed')
        return clean_data


    # def save(self, commit=True):
    #     request = self.request
    #     data = self.cleaned_data
    #     password = data.get("password")
    #     user_objects = User.objects.filter(email=email)
    #     if not user_objects.exists(): 
    #         username = User.objects.check_username(username=email.split("@")[0])
    #         User.objects.create_user(email=email, username=username, password=password, is_active=False)

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'is_active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class GuestForm(forms.ModelForm):
	# email = forms.EmailField()
    class Meta:
        model = GuestEmail
        fields = [
            'email'
        ]
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(GuestForm,self).__init__(*args,**kwargs)

    def save(self, commit=True):
        # Save the provided password in hashed format
        obj = super(GuestForm, self).save(commit=False)
        if commit:
            obj.save()
            request = self.request
            request.session['guest_email_id'] = obj.id
        return obj



class RegisterLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
    email = forms.CharField(
        widget=forms.EmailInput(), label='')
    password = forms.CharField(label='', widget=forms.PasswordInput())

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(RegisterLoginForm,self).__init__(*args,**kwargs)
        self.fields['password'].widget.attrs['placeholder'] = _('Min 8 characters, digits + numbers')
        self.fields['email'].widget.attrs['placeholder'] = _('Your Email')
    def clean(self):
        link = reverse("accounts:resend-activation")
        reconfirm_msg = _("""Go to <a href='{resend_link}'>resend confirmation email</a>.""").format(resend_link=link)
        self.cleaned_data['msg'] = reconfirm_msg                            

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password, self.instance)
        except forms.ValidationError as error:
            # Method inherited from BaseForm
            self.add_error('password', error)
        return self.cleaned_data.get('password')


    # def clean_subscribed(self):
    #     marketing_pref = MarketingPreference.objects.filter(user=self.request.user)
    #     subscribed_user = self.cleaned_data.get('subscribed')
    #     marketing_pref.update(subscribed=subscribed_user)

    def save(self, commit=True):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        user_objects = User.objects.filter(email=email)
        if not user_objects.exists(): 
            username = User.objects.check_username(username=email.split("@")[0])
            User.objects.create_user(email=email, username=username, password=password, is_active=False)


class RegionModalForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('region',)
    location = forms.CharField(required=False, widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(RegionModalForm, self).__init__(*args, **kwargs)
        self.fields['location'].widget.attrs['readonly'] = True
        self.fields['location'].widget.attrs['value'] = self.request.GET.get('location')
        print(self.request.POST)
    def save(self):
        user = self.request.user
        region = self.cleaned_data.get('region')
        user.region = region
        user.save()



        




#----Deleting guest mails if there are any-----------------
    # user_logged_in_signal.send(user.__class__, instance = user, request = request)
    # try:
    #     del request.session['guest_email_id']
    # except:
    #     pass


    # if user is None:
    #     raise forms.ValidationError("Oops... something went wrong. Please contact us!")

#-------------ACTIVE-FALSE-----------------


 