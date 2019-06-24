from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.urlresolvers import reverse
import re 
User = get_user_model()

from .models import EmailActivation, GuestEmail
from .signals import user_logged_in_signal

class ReactivateEmailForm(forms.Form):
    error_css_class = 'error'
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_objects = EmailActivation.objects.email_exists(email)
        if not user_objects.exists():
            reset_link = reverse("register")
            msg = """This Email does not exist. Would you like to <a href="{link}">register</a>?
            """.format(link=reset_link)
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


from marketing.models import MarketingPreference


class MarketingPreferenceForm(forms.ModelForm):
    subscribed = forms.BooleanField(label = 'Recieve marketing email?', required=False)
    class Meta:
        model = MarketingPreference
        fields = [
            'subscribed',

        ]

class UserDetailChangeForm(forms.ModelForm):
    username  = forms.CharField(label='Username', required=True, widget=forms.TextInput(attrs={"class":'form-control'}))
    full_name = forms.CharField(label='Name', required=False, widget=forms.TextInput(attrs={"class":'form-control'}))
    class Meta:
        model = User
        fields = [
                'username',
                'full_name',
                'profile_foto'
                    ]
    def __init__(self, request, *args, **kwargs):
        super(UserDetailChangeForm, self).__init__(*args, **kwargs)
        self.lan = request.session.get('language')
        if self.lan == 'RU':
            self.fields['username'].label = "Имя пользователя"
            self.fields['full_name'].label = "Имя и фамилия"
            self.fields['profile_foto'].label = "Фото профиля"
    def clean_username(self):
        data = self.cleaned_data['username']
        contains_rus = bool(re.search('[а-яА-Я]', data))
        if contains_rus:
            raise forms.ValidationError("Имя пользователя должно содержать только латинские символы")
        return data


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
        widget=forms.EmailInput(
        attrs={'placeholder': 'Your Email'}), label=''
        )
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Min 8 characters, digits + numbers'}))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(RegisterLoginForm,self).__init__(*args,**kwargs)
        if request.session.get('language') == 'RU':
            self.fields['password'].widget.attrs['placeholder'] = 'Минимум 8 символов + цифры'
            self.fields['email'].widget.attrs['placeholder'] = 'Ваш Email'

    def clean(self):
        link = reverse("accounts:resend-activation")
        if self.request.session.get('language') == 'RU':
            reconfirm_msg = """<a href='{resend_link}'> (Кликните, чтобы выслать подтверждение еще раз</a>.)""".format(resend_link=link)
        else:
            reconfirm_msg = """Go to <a href='{resend_link}'>resend confirmation email</a>.""".format(resend_link=link)
        self.cleaned_data['msg'] = reconfirm_msg                            

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password, self.instance)
        except forms.ValidationError as error:
            # Method inherited from BaseForm
            self.add_error('password', error)
        return self.cleaned_data.get('password')



    def save(self, commit=True):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        user_objects = User.objects.filter(email=email)
        if not user_objects.exists(): 
            username = User.objects.check_username(username=email.split("@")[0])
            User.objects.create_user(email=email, username=username, password=password, is_active=False)





#----Deleting guest mails if there are any-----------------
    # user_logged_in_signal.send(user.__class__, instance = user, request = request)
    # try:
    #     del request.session['guest_email_id']
    # except:
    #     pass


    # if user is None:
    #     raise forms.ValidationError("Oops... something went wrong. Please contact us!")

#-------------ACTIVE-FALSE-----------------





 