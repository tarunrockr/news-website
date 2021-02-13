from __future__ import unicode_literals
from django.db import models
from category.models import Category

# Create your models here.

class SubCategory(models.Model):
	
	name            = models.CharField(max_length=100, null=True)
	category_name   = models.CharField(max_length=100, null=True)
	category        = models.ForeignKey(Category, on_delete = models.CASCADE)
	
	def __str__(self):
		return self.name
	


