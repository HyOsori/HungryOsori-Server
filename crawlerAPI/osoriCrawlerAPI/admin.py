from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserProfileCreationForm, UserProfileChangeForm
from .models import UserProfile, Crawler

class UserProfileAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserProfileChangeForm
    add_form = UserProfileCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'is_active', 'is_admin', 'created', 'last_login')
    list_display_links = ('email',)
    list_filter = ('is_admin', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', )}),
        ('Permissions', {'fields': ('is_active', 'is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
         ),
    )
    search_fields = ('email','name')
    ordering = ('-created',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Crawler)

#admin.site.unregister(Group)