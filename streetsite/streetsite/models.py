from django.db import models
from django.contrib import admin

class Fight(models.Model):
    word = models.TextField()
    ip = models.TextField()

class BadFight(models.Model):
    word = models.TextField()
    ip = models.TextField()
