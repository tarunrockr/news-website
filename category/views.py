from django.shortcuts import render, get_object_or_404, redirect 
from .models import Category
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
# Create your views here.


def category_list(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	category = Category.objects.all()
	return render( request, 'category/back/category_list.html', { 'category_list': category } )


def create_category(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	return render(request, 'category/back/add_category.html', {} )


def store_category(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	if request.method == "POST":

		name = request.POST.get("name")
		#return HttpResponse(name)


		# Custom Validation
		Error_dict = {}
		if name == "":
			Error_dict.update({'name': "Category Title field required"})

		if len(Category.objects.filter(name=name)) > 0 :
			Error_dict.update({'name_exist': "Category Title already exists"})

		if len(Error_dict) != 0:
			return render(request, 'category/back/add_category.html',{'error':Error_dict})

		category = Category( name = name )
		category.save()

		messages.success(request, "New Category Added")
		return redirect(reverse('category.create'))


	else:

		pass



