from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Category(models.Model):
	
	name       = models.CharField(max_length=100, null=True)
	count      = models.IntegerField(default='0' , null=True)
	
	def __str__(self):
		return self.name
	

