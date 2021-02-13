from django.shortcuts import render, get_object_or_404, redirect 
from .models import SubCategory
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.db import connection
from category.models import Category
# Create your views here.


def subcategory_list(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	#subcategory = SubCategory.objects.all().select_related()
	#or
	#subcategory = SubCategory.objects.raw("SELECT * FROM subcategory_subcategory")
	cursor = connection.cursor()
	sql    = '''
				SELECT subcat.*,cat.name as category FROM subcategory_subcategory subcat
						 LEFT JOIN category_category cat ON cat.id = subcat.category_id 
			 '''
	cursor.execute(sql)
	subcategory = cursor.fetchall()

	return render( request, 'subcategory/back/subcategory_list.html', { 'sub_category_list': subcategory } )


def create_subcategory(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	category_list = Category.objects.all()

	return render(request, 'subcategory/back/add_subcategory.html', {'category_list': category_list} )


def store_subcategory(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	if request.method == "POST":

		name        = request.POST.get("name")
		category_id = request.POST.get("category")
		#return HttpResponse(category_id)


		# Custom Validation
		Error_dict = {}
		if name == "":
			Error_dict.update({'name': "SubCategory Title field required"})

		if len(SubCategory.objects.filter(name=name)) > 0 :
			Error_dict.update({'name_exist': "SubCategory Title already exists"})

		if category_id == "":
			Error_dict.update({'category': "Category field required"})

		if len(Error_dict) != 0:
			category_list = Category.objects.all()
			return render(request, 'subcategory/back/add_subcategory.html',{'error':Error_dict, 'category_list': category_list})

		category_data = Category.objects.get(pk=category_id)

		subcategory = SubCategory( name = name, category_id = category_id, category_name = category_data.name )
		subcategory.save()

		messages.success(request, "New subcategory added successfully")
		return redirect(reverse('subcategory.create'))


	else:

		pass



