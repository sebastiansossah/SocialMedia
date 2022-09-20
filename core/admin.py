from django.contrib import admin
from core.models import post, profile, likePost, followsModel

# Register your models here.

admin.site.register(profile)
admin.site.register(post)
admin.site.register(likePost)
admin.site.register(followsModel)