from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    task = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task

    class Meta:

        ordering = ('is_completed',)


#
# Username (leave blank to use 'moury'): shyam
# Email address: shyam@gmail.com
# Password: abc
# Password (again):
