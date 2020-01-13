from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

#Register your models here.




class CategoryAdmin(admin.ModelAdmin):

    list_display = ('id','name')


admin.site.register(Article)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Comment)
admin.site.register(User_like)
# admin.site.register(UserGroup)
#admin.site.register(UserProfile)
# admin.site.register(UserProfile,UserAdmin)


