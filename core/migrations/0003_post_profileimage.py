# Generated by Django 4.0.6 on 2022-09-14 01:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='profileImage',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='profile_images'),
            preserve_default=False,
        ),
    ]
