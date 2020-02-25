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
        ('4', 'Restored')
    ]
    status = models.CharField(choices=STATUS_CHOICES,max_length=2,default='1')
    RESOLUTION_CHOICES = [
        ('1', 'Resolved'),
        ('2', 'Rejected')
    ]
    resolution = models.CharField(choices=RESOLUTION_CHOICES,max_length=2,null=True,blank=True)
    flag_delete = models.BooleanField(default=False)
    flag_reopen = models.BooleanField(default=False)


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    request = models.ForeignKey(Request,on_delete=models.CASCADE,default='')
    text = models.CharField(max_length=200)
    date_comment = models.DateTimeField(auto_now_add=True)


class Event(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.DO_NOTHING,related_name='request_name')
    EVENT_CHOICES = [
        ('1', 'Create Request'),
        ('2', 'Update Request'),
        ('3', 'Create Comment'),
        ('4', 'Update Comment'),
        ('5', 'Update Status')
    ]
    event = models.CharField(choices=EVENT_CHOICES, max_length=2, default='1')
    event_date_time = models.DateTimeField(auto_now_add=True)

    def create_event(user,request,event,event_date_time):
        event = Event.objects.create(user=user, request=request, event=event,event_date_time=event_date_time)
        event.save()







