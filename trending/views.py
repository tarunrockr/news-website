from  django.shortcuts import render, get_object_or_404, redirect 
from .models import Trending
from  news.models import News
from  category.models import Category
from  subcategory.models import SubCategory
from  django.db import connection
from  django.http import HttpResponse 
from  django.urls import reverse
from  django.contrib.auth import authenticate, login, logout
from  django.core.files.storage import FileSystemStorage
from  django.contrib import messages
from  datetime import datetime

#Admin functions
def create_trending(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	trending_list = Trending.objects.all().order_by('-pk')[:5]

	return render(request, 'trending/back/create_trending.html', {'trending_list': trending_list})

def store_trending(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	if request.method == "POST":

		trending_text = request.POST.get('trending_text')

		# Custom Validation
		Error_dict = {}
		if trending_text == "":
			Error_dict.update({'trending_text': "News Title field required"})

		if len(Error_dict) != 0:
			return render(request, 'trending/back/create_trending.html', {'error': Error_dict})


		trending = Trending(text = trending_text  )
		trending.save()

		messages.success(request, 'Trending News Added Successfully')
		return redirect(reverse('trending.create'))


def edit_trending(request, id):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	try:

		edit_trending = Trending.objects.get(pk=id)
		return render(request, 'trending/back/edit_trending.html', {'edit_trending': edit_trending} )

	except:

		messages.error("Technical error occured!")
		return redirect(reverse('trending.create'))


def update_trending(request, id):


	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	if request.method == "POST":

		trending_text = request.POST.get('trending_text')

		# Custom Validation
		Error_dict = {}
		if trending_text == "":
			Error_dict.update({'trending_text': "News Title field required"})

		if len(Error_dict) != 0:
			edit_trending = Trending.objects.get(pk=id)
			return render(request, 'trending/back/edit_trending.html', {'error': Error_dict, 'edit_trending': edit_trending})

		trending      = Trending.objects.get(pk=id)
		trending.text = trending_text
		trending.save()

		messages.success(request, "Trending news updated successfully!")
		return redirect(reverse('trending.create'))



def trending_delete(request, id):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	try:
		trending = Trending.objects.get(pk=id)
		trending.delete()

		messages.success(request, 'Trending news deleted Successfully')
		return redirect(reverse(trending.create))

	except:
		messages.error(request, 'Technical error occured!')
		return redirect(reverse('trending.create'))


