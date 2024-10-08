# Generated by Django 5.0.1 on 2024-05-24 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bfaWebBlog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='posts', to='bfaWebBlog.tags'),
        ),
    ]
