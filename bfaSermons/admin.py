from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
from .models import *


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    list_display = ['title']

@admin.register(BibleBook)
class BibleBookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ['name']

admin.site.register(Sermon_Category)
admin.site.register(VideoDownload)





