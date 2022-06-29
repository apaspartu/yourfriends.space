from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Post(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='published_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, null=False, default='There is nothing yet...')
    birth_date = models.DateField(null=False, default='2000-12-01')
    photo = CloudinaryField('image', null=True)

    def __str__(self):
        return str(self.user)


class Follow(models.Model):
    link_id = models.AutoField(primary_key=True)
    first_user_id = models.IntegerField(unique=False, null=True)
    second_user_id = models.IntegerField(unique=False, null=True)


    def __str__(self):
        return f'{self.first_user_id} follows {str(self.second_user_id)}'
