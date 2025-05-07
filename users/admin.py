# users/admin.py
from django.contrib import admin
from .models import User, Professional, Client

# Define custom actions to approve and reject professional users
def approve_professional(modeladmin, request, queryset):
    queryset.update(status='approved')

def reject_professional(modeladmin, request, queryset):
    queryset.update(status='canceled')

approve_professional.short_description = "Approve selected professionals"
reject_professional.short_description = "Reject selected professionals"

class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'card_number')
    list_filter = ('status',)
    actions = [approve_professional, reject_professional]

class ClientAdmin(admin.ModelAdmin):
    list_display = ('user',)
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'role', 'is_staff', 'is_superuser')
    search_fields = ('email', 'full_name')

# Register the models with the admin site
admin.site.register(User, UserAdmin)
admin.site.register(Professional, ProfessionalAdmin)
admin.site.register(Client, ClientAdmin)
