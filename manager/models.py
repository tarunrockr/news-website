from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Manager(models.Model):
	
	name      = models.CharField(max_length=100, null=True)
	user_text = models.TextField(default='-', null=True)
	email     = models.TextField(default='-', null=True)


	def __str__(self):
		return self.set_name
