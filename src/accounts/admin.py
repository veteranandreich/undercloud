from django.contrib import admin
from .models import User


class AccountsAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_of_registration', 'is_active', 'is_staff')
    list_filter = ['date_of_registration']


admin.site.register(User, AccountsAdmin)
