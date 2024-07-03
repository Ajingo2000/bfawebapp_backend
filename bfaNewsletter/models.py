from django.db import models
from tinymce.models import HTMLField


# Create your models here.
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return self.email
    
class EmailTemplate(models.Model):
    subject = models.CharField(max_length=255)
    message = HTMLField()
    recipients = models.ManyToManyField(Subscriber)

    def __str__(self):
        return self.subject
    

