from __future__ import unicode_literals
from django.db import models
from category.models import Category
from subcategory.models import SubCategory

# Create your models here.

class News(models.Model):
	
	name       = models.CharField(max_length=100, null=True)
	short_text = models.TextField(default='-', null=True)
	body_text  = models.TextField(default='-', null=True)
	date       = models.DateTimeField(null=True)
	picname    = models.TextField(blank=True,null=True)
	picurl     = models.TextField(blank=True,null=True, default='-')
	writer     = models.CharField(max_length=100, null=True)
	catname    = models.CharField(max_length=100, null=True, blank=True, default='-')
	cat        = models.ForeignKey(Category, on_delete = models.CASCADE, null=True, blank=True)
	sub_cat    = models.ForeignKey(SubCategory, on_delete = models.CASCADE, null=True, blank=True)
	show       = models.IntegerField(null=True, blank=True, default=0)
	tag        = models.TextField(null=True, blank=True, default='-')
	active     = models.IntegerField(null=True, blank=True, default='0')

	
	def __str__(self):
		return self.name
	

