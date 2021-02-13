from __future__ import unicode_literals
from django.db import models

# Create your models here.

class ContactForm(models.Model):
	
	name     = models.CharField(max_length=100, null=True)
	email    = models.CharField(max_length=255, null=True)
	message  = models.TextField(null=True)
	date     = models.DateTimeField(null=True)


	def __str__(self):
		return self.name
	

