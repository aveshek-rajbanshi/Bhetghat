from django.contrib import admin
from accounts.models import UserProfile



@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
  list_display = ['user', 'is_free', 'interests', 'updated_at']
  list_filter = ['is_free']
  search_fields = ['user__username']