# Generated by Django 4.0.6 on 2022-08-20 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page3', '0020_post_is_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='reply_to',
            field=models.IntegerField(blank=True, default=-1, null=True),
        ),
    ]
