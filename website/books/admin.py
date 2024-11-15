from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import user

class CustomUserAdmin(UserAdmin):
	model = user
	list_display = ['email', 'first_name', 'last_name', 'dob', 'city', 'country']
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'dob', 'city', 'country')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'dob', 'city', 'country'),
		}),
	)
	search_fields = ('email', 'first_name', 'last_name')
	ordering = ('email',)

admin.site.register(user, CustomUserAdmin)
