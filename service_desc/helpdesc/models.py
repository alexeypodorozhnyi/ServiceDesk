from django.db import models
from django.contrib.auth.models import User


class Request(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    info = models.TextField(null=True,blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_last_update = models.DateTimeField(auto_now_add=True)
    PRIORITY_CHOICES = [
        ('1', 'Low'),
        ('2', 'Medium'),
        ('3', 'High')
    ]
    priority = models.CharField(choices=PRIORITY_CHOICES,max_length=2,default='1')
    STATUS_CHOICES = [
        ('1', 'New'),
        ('2', 'In Progress'),
        ('3', 'Done'),
        ('4', 'Rejected'),
        ('5', 'Restored'),
        ('6', 'Rejected again')
    ]
    status = models.CharField(choices=STATUS_CHOICES,max_length=2,default='1')
    flag_delete = models.BooleanField(default=False)


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    request = models.ForeignKey(Request,on_delete=models.CASCADE,default='')
    text = models.CharField(max_length=200)
    date_comment = models.DateTimeField(auto_now_add=True)


class StatusHistory(models.Model):
    request = models.ForeignKey(Request,on_delete=models.CASCADE, db_index=True)
    STATUS_CHOICES = [
        ('1', 'New'),
        ('2', 'In Progress'),
        ('3', 'Done'),
        ('4', 'Rejected'),
        ('5', 'Restored'),
        ('6', 'Rejected again')
    ]
    status = models.CharField(choices=STATUS_CHOICES, max_length=2, default='1')
    date_from = models.DateTimeField(auto_now_add=True)





