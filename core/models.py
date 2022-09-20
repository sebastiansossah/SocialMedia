from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.

class profile(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileImg = models.ImageField(upload_to='profile_images', default= 'MyBlank.jpg')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
        
class post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to="Post_images")
    caption = models.TextField()
    created_at = models.DateTimeField(default= datetime.now)
    number_likes = models.IntegerField(default= 0)
    profileImage = models.ImageField(upload_to='profile_images', default= 'MyBlank.jpg' )

    def __str__(self):
        return self.user

class likePost(models.Model):
    post_id = models.CharField(max_length=600)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class followsModel(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
