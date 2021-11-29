from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.deletion import CASCADE

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    
    REQUIRED_FIELDS = []



class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host=models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    topic=models.ForeignKey(Topic,null=True, on_delete=models.SET_NULL)# specify Room as children for Topic
    name=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    participants=models.ManyToManyField(User,related_name='participants',blank=True)#manytomany is for select one more obj
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)


    class Meta:
        #(minus)-updated is for acsending based on last created or updated
        ordering=['-updated','-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    room=models.ForeignKey(Room, on_delete=models.CASCADE)# specify message as children for room
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    

    class Meta:
        #(minus)-updated is for acsending based on last created or updated
        ordering=['-updated','-created']
        
            
    def __str__(self):
        return self.body[0:50]
