from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.safestring import mark_safe
from django.contrib.auth.password_validation import validate_password
from django.core.urlresolvers import reverse
from django.utils.translation import gettext as _ 
from django.utils.translation import pgettext

from marketing.models import MarketingPreference
from .models import EmailActivation, Region
from ecommerce.utils import alphanumeric
from django import forms

from django.contrib.auth.forms import PasswordChangeForm


User = get_user_model()


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

    class Meta:
        model = User
        fields = ('full_name', 'email',)


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

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
    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()

    def save(self, commit=True):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        user_objects = User.objects.filter(email__iexact=email)
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
        self.fields['region'].label = False
    def save(self):
        user = self.request.user
        region = self.cleaned_data.get('region')
        user.region = region
        user.save()

class UserDetailChangeForm(forms.ModelForm): 
    username  = forms.CharField(required=True, widget=forms.TextInput(attrs={"class":'form-control labels-placement'}))
    region = forms.ChoiceField(widget=forms.Select(attrs={"class":'labels-placement'}), required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":'form-control labels-placement', 'disabled':'true'}), required=False)
    subscribed = forms.BooleanField(required=False)
    profile_foto = forms.FileField(required=False, widget=forms.FileInput(attrs={'class':'avatar-upload-button','id':'avatar_custom'} ))

    class Meta:
        model = User
        fields = [
                'username',
                'region',
                'profile_foto',
                'bio',
                    ]
        widgets = {
          'bio': forms.Textarea(attrs={
                'rows':4,
                'cols':15,
                'placeholder':_('Use this space to talk about your personal style but hold the personal contact details')
            }),
        }

    def get_region_choices(self):
        t = Region.objects.values_list('region', flat=True)
        region_choices = list(zip(t, t))
        region_choices.append(tuple(('default', _('-- Please select your region --')))) #append default value
        return region_choices


    def __init__(self, request, *args, **kwargs):
        super(UserDetailChangeForm, self).__init__(*args, **kwargs)
        self.request = request
        user = request.user

        self.fields['email'].label = _('Email')
        self.fields['username'].label = _('Username')
        self.fields['region'].label = _('Region')
        self.fields['subscribed'].label = _('Recieve marketing email?')



        self.fields['username'].validators = [alphanumeric]
        self.fields['profile_foto'].widget.attrs['label_for_btn'] = pgettext('profile_update','Update')

        self.initial['region'] = user.region
        if self.initial['region'] is None: 
            self.initial['region'] = ('default', _('-- Please select your region --'))
        self.fields['region'].choices = self.get_region_choices()
        self.fields['email'].initial= user.email

        self.fields['subscribed'].initial= user.marketing.subscribed
        self.fields['subscribed'].widget.attrs['class']='custom-checkbox'
        self.fields['bio'].label = False
        self.fields['profile_foto'].label = False


    def clean_subscribed(self):
        MarketingPreference.objects.filter(user=self.request.user).update(subscribed=self.cleaned_data.get('subscribed'))

    def clean_region(self):
        data = self.cleaned_data['region']
        if data == 'default' or data == '':
            raise forms.ValidationError(_("You must select a region"))
        return Region.objects.filter(region=data).first()

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control labels-placement'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control labels-placement'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":'form-control labels-placement'}))

    def __init__(self,  *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = _('Old password')
        self.fields['new_password1'].label = _('New password')
        self.fields['new_password1'].help_text = _('Min 8 characters, digits + numbers')
        self.fields['new_password2'].label = _('Confirm password')

