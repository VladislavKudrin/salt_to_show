from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.core.urlresolvers import reverse
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


class UserDetailChangeForm(forms.ModelForm):
    username  = forms.CharField(label='Username', required=True, widget=forms.TextInput(attrs={"class":'form-control'}))
    full_name = forms.CharField(label='Name', required=False, widget=forms.TextInput(attrs={"class":'form-control'}))
    class Meta:
        model = User
        fields = [
                'full_name',
                'username',
                'profile_foto'
                    ]

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
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Your Password'}))

    def __init__(self, request, *args, **kwargs):
        link = reverse("accounts:resend-activation")
        reconfirm_msg="""Go to <a href='{resend_link}'>resend confirmation email</a>.""".format(resend_link=link)
        self.request = request
        super(RegisterLoginForm,self).__init__(*args,**kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        user_objects = User.objects.filter(email=email)
        if user_objects.filter(is_active=False).exists(): 
            link = reverse("accounts:resend-activation")
            reconfirm_msg="""Go to <a href='{resend_link}'>resend confirmation email</a>.""".format(resend_link=link)
            confirm_email=EmailActivation.objects.filter(email=email) #not activated email?
            link_sent = confirm_email.confirmable().exists()
            if link_sent:
                msg1 = "Please check your email to confirm your account. " + reconfirm_msg
                messages.add_message(request, messages.SUCCESS, mark_safe(msg1))

        #------------Not activated email?------------
            link_sent2 = EmailActivation.objects.email_exists(email).exists() #link_sent2 
            if link_sent2:
                msg2 = "Email not confirmed. " +reconfirm_msg
                messages.add_message(request, messages.DEBUG, mark_safe(msg1))

        #------------No link sent to this email------
            if not link_sent and not link_sent2:
                raise forms.ValidationError("Please try with another email.")
        return data

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





 