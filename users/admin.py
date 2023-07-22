from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export.admin import ExportActionMixin
from .models import User


class UserAdmin(ExportActionMixin, BaseUserAdmin):

    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ( 'name', 'email', 'phone_number', 'isVerified', 'usertype', 'appversion', 'admin', )
    list_display_links = ( 'name', 'email', 'phone_number', 'isVerified', 'admin', 'usertype', 'admin', )
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'usertype', 'phone_number', 'isVerified' , 'isCustomer', 'is_deleted', 'OTP', 'appversion', 'status')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'phone_number', 'email', 'isCustomer', 'usertype', 'password1', 'password2',)}
        ),
    )

    def get_inline_instances(self, request, obj=None):
        return [inline(self.model, self.admin_site) for inline in self.inlines]

    search_fields = ('email', 'phone_number')
    ordering = ('email', 'phone_number')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)