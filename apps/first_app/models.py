from django.db import models

class Users(models.Model):
  first_name=models.CharField(max_length=100)
  last_name=models.CharField(max_length=100)
  email=models.CharField(max_length=100)
  password=models.CharField(max_length=255)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

class Quotes(models.Model):
  author=models.CharField(max_length=225)
  quote=models.TextField()
  submitted_by=models.ForeignKey(Users, related_name="quote_made")
  liked_by=models.ManyToManyField(Users, related_name="like_made", null=True)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
