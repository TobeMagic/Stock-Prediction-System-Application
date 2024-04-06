from django.contrib import admin

from .models import UserProfile
from django.utils.safestring import mark_safe


# Register your models here.
# 
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_photo_tag', 'gender', 'tel']

    def profile_photo_tag(self, obj):
        if obj.profile_photo:
            return mark_safe(  # obj.picture 是相对路径, obj.picture.url是完整路径
                f'<image src="{obj.profile_photo.url}"style="width:80px; height:80px;object-fit: cover;" alt="个人图片" value="个人图片" />')
        return '-'
    profile_photo_tag.short_description = '用户头像'
# admin.site.register(UserProfile)
