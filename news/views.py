from django.shortcuts import render, get_object_or_404, redirect 
from .models import News
from django.http import HttpResponse, JsonResponse
import datetime
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from category.models import Category
from subcategory.models import SubCategory
from django.db import connection
from django.http import JsonResponse
# Create your views here.


def news_detail(request, news_id):

	news = News.objects.all().order_by('-pk')
	popnews = News.objects.all().order_by('-show')
	cursor = connection.cursor()
	category_sql = '''
					SELECT cat.*, ( SELECT COUNT(*) FROM news_news as news WHERE news.cat_id = cat.id ) as cat_count 
						FROM category_category as cat
				   '''
	cursor.execute(category_sql)
	category = cursor.fetchall()
	#return HttpResponse(category)
	#category = Category.objects.all()
	subcategory = SubCategory.objects.all()

	main_news = News.objects.get(pk=news_id)

	# Increasing the views
	main_news.show =  main_news.show + 1
	main_news.save()

	tag_string = News.objects.get(pk=news_id).tag
	tags       = tag_string.split(',') 

	context = { 'title': 'MySite | News Detail', 'news': news, 'main_news': main_news, 'category': category, 'subcategory': subcategory, 'popnews': popnews, 'tags': tags }
	return render(request, 'news/front/news_detail.html', context)


# Admin news list
def news_list(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	#news = News.objects.all().select_related()
	# 2nd way to fetch data
	cursor = connection.cursor() 
	sql = '''
			SELECT news.*, cat.name as 'category_name', subcat.name as 'subcategory_name' 
			FROM news_news as news
			LEFT JOIN category_category as cat ON cat.id = news.cat_id 
			LEFT JOIN subcategory_subcategory as subcat ON subcat.id = news.sub_cat_id
		  '''
	cursor.execute(sql)
	news   = cursor.fetchall()
	#return HttpResponse(news);
	return render(request, 'main/back/news_list.html', {'allnews': news} )


# Admin create news
def add_news(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	category = Category.objects.all()
	return render(request, 'main/back/add_news.html', { 'category': category } )

# Admin store news
def store_news(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	if request.method == "POST":

		news_title      = request.POST.get('news_title')
		news_category   = request.POST.get('news_category')
		news_subcategory= request.POST.get('news_subcategory')
		news_text_short = request.POST.get('news_text_short')
		news_text       = request.POST.get('news_text')
		tag             = request.POST.get('tag')

		# Date process. START

		now   = datetime.datetime.now()

		year  = now.year
		month = now.month
		day   = now.day

		if len(str(day)) == 1:
			day = "0" + str(day)

		if len(str(month)) == 1:
			month = "0" + str(month)


		today = str(year) + '/' + str(month) + '/' + str(day)



		# Date process. END

		# if news_title == "" or news_text_short == "" or news_text == "" or news_category=="":
		# 	error = "All fields are required"
		# 	return render(request, 'main/back/error.html', { 'error': error } )

		# Custom Validation
		Error_dict = {}
		if news_title == "":
			Error_dict.update({'news_title': "News Title field required"})
		if news_category == "":
			Error_dict.update({'news_category': "News Category field required"})
		if news_subcategory == "":
			Error_dict.update({'news_subcategory': "News SubCategory field required"})
		if news_text_short == "":
			Error_dict.update({'news_text_short': "News Short Text field required"})
		if news_text == "":
			Error_dict.update({'news_text': "News Text field required"})

		if len(Error_dict) != 0:
			category = Category.objects.all()
			return render(request, 'main/back/add_news.html',{'error':Error_dict, 'category':category})

		#try:
			# Uploading files
		newsfile = request.FILES['newsfile'] if 'newsfile' in request.FILES else None
		file = ''
		fileurl = ''
		if newsfile:

			if newsfile.size > 5000000:

				Error_dict.update({'newsfile': "Your file is bigger than 5 MB"})
				category = Category.objects.all()
				return render(request, 'main/back/add_news.html',{'error':Error_dict, 'category':category})


			if str(newsfile.content_type).startswith('image'):
			 
				# create a new instance of FileSystemStorage
					fs = FileSystemStorage()
				# save attatched file
					file = fs.save(newsfile.name, newsfile)
				# The fileurl variable now contains the url to the file. This can be used to serve the file when needed.
					fileurl = fs.url(file)

			else:

				Error_dict.update({'newsfile': "News File format not supported"})
				category = Category.objects.all()
				return render(request, 'main/back/add_news.html',{'error':Error_dict, 'category':category})


		# except:
		# 	error = "Error occured in file upload"
		#     return render(request, 'main/back/error.html', { 'error': error } )

		category_data = Category.objects.get(pk=news_category)
		news = News(name = news_title, short_text = news_text_short, body_text = news_text, date = datetime.datetime.now(), picname=file, picurl = fileurl, writer = request.user, catname = category_data.name, cat_id = news_category, sub_cat_id = news_subcategory, show= 0, tag = tag )
		news.save()

		messages.success(request, 'News Added Successfully')
		return redirect(reverse('news.add'))
		#return redirect(reverse('url_to_redirect_to', kwargs={'args_1':value}))
		#return redirect(add_news)


	# return HttpResponse(str('GET'))


# Admin edit news
def edit_news(request, id):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	if len(News.objects.filter(pk=id)) == 0 :
		cursor = connection.cursor() 
		sql = '''
				SELECT news.*, cat.name as 'category_name', subcat.name as 'subcategory_name' 
				FROM news_news as news
				LEFT JOIN category_category as cat ON cat.id = news.cat_id 
				LEFT JOIN subcategory_subcategory as subcat ON subcat.id = news.sub_cat_id
			  '''
		cursor.execute(sql)
		news   = cursor.fetchall()
		messages.warning(request, 'News not exists')
		return render(request, 'main/back/news_list.html', {'allnews': news} )

	category = Category.objects.all()
	news     = News.objects.get(pk=id)
	return render(request, 'main/back/edit_news.html', { 'category': category, 'edit_data': news } )

# Admin update news
def update_news(request, id):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	if request.method == "POST":

		news_title      = request.POST.get('news_title')
		news_category   = request.POST.get('news_category')
		news_subcategory= request.POST.get('news_subcategory')
		news_text_short = request.POST.get('news_text_short')
		news_text       = request.POST.get('news_text')
		tag             = request.POST.get('tag')

		# Custom Validation
		Error_dict = {}
		if news_title == "":
			Error_dict.update({'news_title': "News Title field required"})
		if news_category == "":
			Error_dict.update({'news_category': "News Category field required"})
		if news_subcategory == "":
			Error_dict.update({'news_subcategory': "News SubCategory field required"})
		if news_text_short == "":
			Error_dict.update({'news_text_short': "News Short Text field required"})
		if news_text == "":
			Error_dict.update({'news_text': "News Text field required"})

		if len(Error_dict) != 0:
			category = Category.objects.all()
			news     = News.objects.get(pk=id)
			return render(request, 'main/back/edit_news.html',{'error':Error_dict, 'category':category, 'edit_data': news})


		# Uploading files
		newsfile = request.FILES['newsfile'] if 'newsfile' in request.FILES else None
		file = ''
		fileurl = ''
		if newsfile:

			if newsfile.size > 5000000:

				Error_dict.update({'newsfile': "Your file is bigger than 5 MB"})
				category = Category.objects.all()
				news     = News.objects.get(pk=id)
				return render(request, 'main/back/add_news.html',{'error':Error_dict, 'category':category, 'edit_data': news})


			if str(newsfile.content_type).startswith('image'):
			 
				# create a new instance of FileSystemStorage
				fs = FileSystemStorage()
				# save attatched file
				file = fs.save(newsfile.name, newsfile)
				# The fileurl variable now contains the url to the file. This can be used to serve the file when needed.
				fileurl = fs.url(file)

			else:
				Error_dict.update({'newsfile': "News File format not supported"})
				category = Category.objects.all()
				news     = News.objects.get(pk=id)
				return render(request, 'main/back/add_news.html',{'error':Error_dict, 'category':category, 'edit_data': news})


		# Saving to database
		category_data      = Category.objects.get(pk=news_category)
		news               = News.objects.get(pk=id)

		news.name          = news_title
		news.short_text    = news_text_short
		news.body_text     = news_text
		if file != "":
			news.picname   = file
			news.picurl    = fileurl
		news.writer        = '-'
		news.catname       = category_data.name
		news.cat_id        = news_category
		news.sub_cat_id    = news_subcategory
		news.tag           = tag
		news.active        = 0
		news.save()

		messages.success(request, 'News Updated Successfully')
		return redirect(reverse('news.edit', kwargs={'id': id} ))



# Admin delete news
def destroy(request, id):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	try:

		news = News.objects.get(pk=id)
		
		# Deleting attached files
		if news.picname != "":
			fs = FileSystemStorage()
			fs.delete(news.picname)

		news.delete()

		messages.success(request, 'News Deleted Successfully.')
		return redirect(reverse('news.list'))
		
	except :

		messages.error(request, 'Error occured')
		return redirect(reverse('news.list'))
		
	
		
# Admin fetch subcategory - Ajax method
def fetch_subcategory_ajax(request):

	category_id      = request.POST.get('category_id')
	subcategory_data = SubCategory.objects.filter(category_id=category_id)
	#return HttpResponse(subcategory_data)

	output = "<option value='' >Select SubCategory</option>"
	if subcategory_data:
		for subcat in subcategory_data:
			output += "<option value='{0}' >{1}</option>".format(subcat.id, subcat.name)
		subcat_dict = {'subcategory': output}

	else:
		subcat_dict = {'subcategory': output }

    
	return JsonResponse(subcat_dict, safe=True)


# Ajax method to toggle the news activation
def activation_toggle_ajax(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	news_id = request.POST.get('news_id')
	active_status = request.POST.get('active_status')

	set_status = 1
	if active_status == '1':
		set_status=0

	try:
		news_data = News.objects.get(pk=news_id)
		news_data.active = set_status
		news_data.save()

		responseData = {
			'st': active_status,
			'change': set_status,
	        'success': '1',
	        'error' : '0',
	        'message': 'Status Updated Successfully'
		}
		return JsonResponse(responseData)
		
	except :

		responseData = {
	        'success': '0',
	        'error' : '1',
	        'message': 'Status could not update'
		}
		return JsonResponse(responseData)





