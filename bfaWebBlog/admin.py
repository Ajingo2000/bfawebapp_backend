from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin



# Register your models here.
class PostAdmin(admin.ModelAdmin):  # instead of ModelAdmin
    prepopulated_fields = {'slug': ('title', )}

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(IpModel)
admin.site.register(Tags)
