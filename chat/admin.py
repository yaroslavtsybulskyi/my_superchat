from django.contrib import admin
from chat.models import Company, Profile


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Company model.
    """

    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Profile model.
    """

    list_display = ('id', 'user', 'company')
    search_fields = ('user__username',)
