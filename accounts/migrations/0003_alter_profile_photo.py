# Generated by Django 4.0.5 on 2022-06-29 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_follow_profile_photo_alter_post_publish_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(null=True, upload_to='media/profile_pictures/'),
        ),
    ]
