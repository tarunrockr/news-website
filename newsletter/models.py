from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Newsletter(models.Model):
	
	emailorphone = models.CharField(max_length=100, null=True)
	status       = models.IntegerField(null=True)
	
	def __str__(self):
		return self.emailorphone
