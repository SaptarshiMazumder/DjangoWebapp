# Generated by Django 4.0.6 on 2022-08-21 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page3', '0025_post_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]
