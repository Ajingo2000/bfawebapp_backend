from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
from .models import *



@admin.register(NewBelieverDocuments)
class NewBelieverDocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ['name']


@admin.register(SoulWinningLessons)
class SoulWinningLessonsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ['name']



@admin.register(DiscipleshipLessons)
class DiscipleshipLessonsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ['name']


@admin.register(DisciplerClassLessons)
class DisciplerClassLessonsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ['name']


@admin.register(BiblicalTheologyLessons)
class BiblicalTheologyLessonsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ['name']


@admin.register(MissionaryLetter)
class MissionaryLetterAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    list_display = ['title']







