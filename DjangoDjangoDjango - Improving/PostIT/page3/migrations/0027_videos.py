# Generated by Django 4.0.6 on 2022-08-21 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page3', '0026_alter_post_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videofile', models.FileField(upload_to='videofiles/')),
            ],
        ),
    ]
