from django.db import models

# Create your models here.
class VideoDownload(models.Model):
    url = models.URLField()
    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
    


# Create your models here.
class Sermon(models.Model):
    slug = models.SlugField(null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="sermon_thumbnails/")
    preview = models.FileField(max_length=255 ,upload_to='preview/', blank=True, null=True)
    preaching_date= models.DateTimeField(null=True, blank=True)
    preached_by = models.CharField(max_length=255, null=True, blank=True)
    bible_text = models.CharField(max_length=255, null=True, blank=True)
    bible_chapter = models.CharField(max_length=255, null=True, blank=True)
    bible_verses= models.CharField(max_length=255, null=True, blank=True)
    embed_code = models.TextField(null=True, blank=True)
    youtube_url = models.TextField(null=True, blank=True)
    sermon_audio = models.FileField(max_length=255 ,upload_to='sermon_audios/')
    upload_date = models.DateTimeField(auto_now_add=True, null=True)
    sermon_category = models.ForeignKey("Sermon_Category", on_delete=models.SET_NULL, blank=True, null=True, related_name="sermons")
    bibleBook = models.ForeignKey("BibleBook", on_delete=models.SET_NULL, blank=True, null=True, related_name="sermons")
    isExpository = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-upload_date']

class BibleBook(models.Model):
    name = models.CharField(max_length=255, null=True)
    slug = models.SlugField(null=True)
    thumbnail = models.ImageField(upload_to="BibleBook_Playlist/")
    

    def __str__(self):
        return self.name
    
class Sermon_Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
