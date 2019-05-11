from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
User = get_user_model()

from .models import EmailActivation, GuestEmail
from .signals import user_logged_in_signal

class ReactivateEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            reset_link = reverse("register")
            msg = """This Email does not exist. Would you like to <a href="{link}">register</a>?
            """.format(link=reset_link)
            raise forms.ValidationError(mark_safe(msg))
        return email

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
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


# class LoginForm(forms.Form):
#     email=forms.EmailField(label='Email')
#     password=forms.CharField(widget=forms.PasswordInput())

#     def __init__(self, request, *args, **kwargs):
#         self.request = request
#         super(LoginForm,self).__init__(*args,**kwargs)

#     def clean(self):
#         request = self.request
#         data = self.cleaned_data
#         email = data.get("email")
#         password = data.get("password")
#         qs = User.objects.filter(email=email)
#         if qs.exists():
#             #user email is registred, check active
#             not_active = qs.filter(is_active=False)
#             if not_active.exists():
#                 ##check email activation
#                 link = reverse("accounts:resend-activation")
#                 reconfirm_msg="""Go to <a href='{resend_link}'>
#                 resend confirmation email</a>.
#                 """.format(resend_link = link)
#                 confirm_email=EmailActivation.objects.filter(email=email)
#                 is_confirmable = confirm_email.confirmable().exists()
#                 if is_confirmable:
#                     msg1 = "Please check your email to confirm your account. "+ reconfirm_msg
#                     raise forms.ValidationError(mark_safe(msg1))
#                 email_confirm_exists_qs = EmailActivation.objects.email_exists(email).exists()
#                 if email_confirm_exists_qs:
#                     msg2 = "Email not confirmed. "+reconfirm_msg
#                     raise forms.ValidationError(mark_safe(msg2))
#                 if not is_confirmable and not email_confirm_exists_qs:
#                     raise forms.ValidationError("This user is inactive")
#         user = authenticate(request, username=email, password=password)
#         if user is None:
#             raise forms.ValidationError("Invelid credentials")
#         login(request, user)
#         self.user = user
#         user_logged_in_signal.send(user.__class__, instance = user, request = request)
#         try:
#             del request.session['guest_email_id']
#         except:
#             pass
#         return data

    # def form_valid(self, form):
    # request = self.request
    # next_ = request.GET.get('next')
    # next_post = request.POST.get('next')
    # redirect_path=next_ or next_post or None
    # email = form.cleaned_data.get("email")
    # password = form.cleaned_data.get("password")        

    # if user is not None:
    #     if not user.is_active:
    #         messages.error(request, "This user is inactive!")
    #         return super(LoginView, self).form_invalid(form)
    #     login(request, user)
    #     user_logged_in_signal.send(user.__class__, instance = user, request = request)
    #     try:
    #         del request.session['guest_email_id']
    #     except:
    #         pass
    #     if is_safe_url(redirect_path, request.get_host()):
    #         return redirect(redirect_path)
    #     else:
    #         return redirect("/")
    # return super(LoginView, self).form_invalid(form)


class RegisterLoginForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    class Meta:
        model = User
        fields = ('email',)

    email = forms.CharField(
        widget=forms.EmailInput(
        attrs={'placeholder': 'Your Email'}), label=''
        )

    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'Your Password'}))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(RegisterLoginForm,self).__init__(*args,**kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        qs = User.objects.filter(email=email)
        if not qs.exists():
            username = email.split("@")[0]
            User.objects.create_user(email=email, username=username, password=password)
        if qs.exists():
            #user email is registred, check active
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                ##check email activation
                link = reverse("accounts:resend-activation")
                reconfirm_msg="""Go to <a href='{resend_link}'>
                resend confirmation email</a>.
                """.format(resend_link = link)
                confirm_email=EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg1 = "Please check your email to confirm your account. "+ reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg1))  
                email_confirm_exists_qs = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists_qs:
                    msg2 = "Email not confirmed. "+reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmable and not email_confirm_exists_qs:
                    raise forms.ValidationError("This user is inactive")
        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError("Invelid credentials")
        login(request, user)
        self.user = user
        user_logged_in_signal.send(user.__class__, instance = user, request = request)
        try:
            del request.session['guest_email_id']
        except:
            pass
        return data

<<<<<<< HEAD
    # def form_valid(self, form):
    # request = self.request
    # next_ = request.GET.get('next')
    # next_post = request.POST.get('next')
    # redirect_path=next_ or next_post or None
    # email = form.cleaned_data.get("email")
    # password = form.cleaned_data.get("password")        

    # if user is not None:
    #     if not user.is_active:
    #         messages.error(request, "This user is inactive!")
    #         return super(LoginView, self).form_invalid(form)
    #     login(request, user)
    #     user_logged_in_signal.send(user.__class__, instance = user, request = request)
    #     try:
    #         del request.session['guest_email_id']
    #     except:
    #         pass
    #     if is_safe_url(redirect_path, request.get_host()):
    #         return redirect(redirect_path)
    #     else:
    #         return redirect("/")
    # return super(LoginView, self).form_invalid(form)


class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    # full_name = forms.CharField(
    #     widget=forms.TextInput(
    #     attrs={'placeholder': 'Your Full Name'}), label=''
    #     )
    email = forms.CharField(
        widget=forms.EmailInput(
        attrs={'placeholder': 'Your Email'}), label=''
        )
    # username = forms.CharField(
    #     widget=forms.TextInput(
    #     attrs={'placeholder': 'Your Username'}), label=''
    #     )
    password1 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'Your Password'}))
    # password2 = forms.CharField(label='', widget=forms.PasswordInput(
    #     attrs={'placeholder': 'Confirm your Password'}))

# class LoginForm(forms.Form):
#     email=forms.EmailField(label='Email')
#     password=forms.CharField(widget=forms.PasswordInput())

#     def __init__(self, request, *args, **kwargs):
#         self.request = request
#         super(LoginForm,self).__init__(*args,**kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        qs = User.objects.filter(email=email)
        if qs.exists():
            #user email is registred, check active
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                ##check email activation
                link = reverse("accounts:resend-activation")
                reconfirm_msg="""Go to <a href='{resend_link}'>
                resend confirmation email</a>.
                """.format(resend_link = link)
                confirm_email=EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg1 = "Please check your email to confirm your account. "+ reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg1))
                email_confirm_exists_qs = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists_qs:
                    msg2 = "Email not confirmed. "+reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmable and not email_confirm_exists_qs:
                    raise forms.ValidationError("This user is inactive")
        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError("Invelid credentials")
        login(request, user)
        self.user = user
        user_logged_in_signal.send(user.__class__, instance = user, request = request)
        try:
            del request.session['guest_email_id']
        except:
            pass
        return data

        
    class Meta:
        model = User
        fields = ('email',)

    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password2

=======
>>>>>>> 3f04dcfd8bd18e9b4c1f30c2a729790f730d6cd9
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterLoginForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active=False #confirmation email
        # obj, is_created = EmailActivation.objects.create(user=user)
        # obj.send_activation_email()
        if commit:
            user.save()
        return user











 