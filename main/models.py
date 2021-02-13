from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Main(models.Model):
	
	name  = models.CharField(max_length=100, null=True)
	about = models.TextField(default='-', null=True)
	about_text = models.TextField(null=True, blank=True, default='-')
	fb = models.CharField(max_length=100, default='-', null=True, blank=True)
	tw = models.CharField(max_length=100, default='-', null=True, blank=True)
	yt = models.CharField(max_length=100, default='-', null=True, blank=True)
	tell = models.CharField(max_length=100, default='-', null=True, blank=True)
	link = models.CharField(max_length=100, default='-', null=True, blank=True)

	set_name = models.CharField(max_length=100, default='-', null=True, blank=True)

	picurl    = models.TextField(default='-',null=True, blank=True)
	picname   = models.TextField(default='-',null=True, blank=True)

	def __str__(self):
		return self.set_name


class Menu(models.Model):

	menu_name = models.CharField(max_length=200, null=True)
	menu_url  = models.CharField(max_length=255, null=True)
	parent    = models.IntegerField(max_length=100, null=True)
	position  = models.IntegerField(max_length=00, null=True)
	menu_icon = models.CharField(max_length=250, null=True)
	status    = models.IntegerField(max_length=100, null=True)
	created_at= models.DateTimeField(auto_now_add=True)
	updated_at= models.DateTimeField(auto_now=True)
	

	

