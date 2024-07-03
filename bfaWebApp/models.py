from django.db import models
import os

# YOUTUBE VIDEO URL 
# downloader/models.py

class NewBelieverDocuments(models.Model):
    name = models.CharField(max_length=255)
    doc_number = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pdf_doc = models.FileField(max_length=255 ,upload_to='New Believer Documents pdfs/')
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

class SoulWinningLessons(models.Model):
    name = models.CharField(max_length=255)
    doc_number = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pdf_doc = models.FileField(max_length=255 ,upload_to='Soul Winning Lessons pdfs/')
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

class DiscipleshipLessons(models.Model):
    name = models.CharField(max_length=255)
    doc_number = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pdf_doc = models.FileField(max_length=255 ,upload_to='Discipleship Lessons pdfs/')
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

class DisciplerClassLessons(models.Model):
    name = models.CharField(max_length=255)
    doc_number = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pdf_doc = models.FileField(max_length=255 ,upload_to='Discipler Class Lessons pdfs/')
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

class BiblicalTheologyLessons(models.Model):
    name = models.CharField(max_length=255)
    doc_number = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pdf_doc = models.FileField(max_length=255 ,upload_to='Biblical Theology Lessons pdfs/')
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

class MissionaryLetter(models.Model):
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField( null=True, blank=True)
    pdf_doc = models.FileField(max_length=255 ,upload_to='Missionary Letter/')
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title

