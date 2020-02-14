from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    post_text = models.TextField(max_length=1000)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, blank=True)
    
class IP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.TextField(max_length=20)

    def __str__(self):
        return self.number

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.TextField(max_length=20)

    def __str__(self):
        return self.number

class Flag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=100)

    def __str__(self):
        return self.name