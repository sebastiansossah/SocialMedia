# Generated by Django 4.0.6 on 2022-09-14 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_post_profileimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='profileImage',
            field=models.ImageField(default='MyBlank.jpg', upload_to='profile_images'),
        ),
    ]
