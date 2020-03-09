from django.contrib import admin

# Register your models here.

from  .models import User, Language


class UserAdmin(admin.ModelAdmin):
    exclude = ('base_user',)
     

admin.site.register(User,UserAdmin)
admin.site.register(Language)
