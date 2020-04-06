from django.contrib import admin
from django.contrib.auth import get_user_model
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import EmailActivation, Wishlist, LanguagePreference, Region

User = get_user_model()

admin.site.register(Wishlist)

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ('email', 'admin', 'timestamp')
    list_filter = ('admin', 'staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Personal info', {'fields': ('profile_foto', 'full_name', 'wishes', 'region')}),
        ('Permissions', {'fields': ('admin', 'staff', 'is_active', )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password')}
        ),
    )
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    filter_horizontal = ()
admin.site.register(User, UserAdmin)

class EmailActivationAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model = EmailActivation
admin.site.register(EmailActivation, EmailActivationAdmin)


class LanguagePreferenceAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'language']
    search_fields = ['user']
    class Meta:
        model = LanguagePreference

admin.site.register(LanguagePreference, LanguagePreferenceAdmin)

admin.site.register(Region)