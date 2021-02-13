from  django.shortcuts import render, get_object_or_404, redirect 
from .models import Main
from  news.models import News
from  category.models import Category
from  subcategory.models import SubCategory
from  django.db import connection
from  django.http import HttpResponse 
from  django.urls import reverse
from  django.contrib.auth import authenticate, login, logout
from  django.core.files.storage import FileSystemStorage
from  django.contrib import messages
from  trending.models import Trending
import random
from random import randint
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from manager.models import Manager

# Create your views here.


def home(request):

	obj = Main.objects.get(pk=1)

	news = News.objects.filter(active=1).order_by('-pk')

	popnews = News.objects.filter(active=1).order_by('-show')

	#return HttpResponse(popnews)

	title = "MySite | "+obj.name

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

	last_three_news = News.objects.filter(active=1).order_by('-pk')[:3]

	trending = Trending.objects.all().order_by('-pk')[:5]

	context = { 'title': title, 'sitedata': obj, 'news': news, 'category': category, 'subcategory': subcategory, 'last_three_news': last_three_news, 'popnews': popnews, 'trending': trending }

	return render(request, 'main/front/home.html', context)



def about(request):

	obj = Main.objects.get(pk=1)
	title = "MySite | "+obj.about


	news = News.objects.all().order_by('-pk')
	popular_news = News.objects.all().order_by('-show')
	cursor = connection.cursor()
	category_sql = '''
					SELECT cat.*, ( SELECT COUNT(*) FROM news_news as news WHERE news.cat_id = cat.id ) as cat_count 
						FROM category_category as cat
				   '''
	cursor.execute(category_sql)
	category = cursor.fetchall()
	subcategory = SubCategory.objects.all()
	trending = Trending.objects.all().order_by('-pk')[:5]

	context = { 'title': title, 'sitedata': obj, 'news': news, 'category': category, 'subcategory': subcategory, 'popnews': popular_news, 'trending': trending }

	return render(request, 'main/front/about.html', context)


def show_contact(request):

	obj = Main.objects.get(pk=1)
	title = "MySite | Contact"

	news = News.objects.all().order_by('-pk')
	popular_news = News.objects.all().order_by('-show')
	cursor = connection.cursor()
	category_sql = '''
					SELECT cat.*, ( SELECT COUNT(*) FROM news_news as news WHERE news.cat_id = cat.id ) as cat_count 
						FROM category_category as cat
				   '''
	cursor.execute(category_sql)
	category = cursor.fetchall()
	subcategory = SubCategory.objects.all()
	trending = Trending.objects.all().order_by('-pk')

	context = { 'title': title, 'sitedata': obj, 'news': news, 'category': category, 'subcategory': subcategory, 'popnews': popular_news, 'trending': trending }

	return render(request, 'main/front/contact.html', context )



# Front Login
def show_login(request):

	return render(request,'main/front/login.html',{})


# Front Login post
def login_submit(request):

	if request.method == 'POST' :

		username= request.POST.get('username')
		password= request.POST.get('password')

		# Custom Validation
		Error_dict = {}
		if username == "":
			Error_dict.update({'username': "Username field required"})

		if password == "":
			Error_dict.update({'password': "Password field required"})

		if len(Error_dict) != 0:
			return render(request, 'main/front/login.html',{'error':Error_dict})

	try:

		user = authenticate(username=username, password=password)

		if user != None :
			login(request, user)
			return redirect(reverse('panel'))
		else:
			messages.error(request, 'Invalid Credentials!')
			return redirect(reverse('login'))
	except:

		messages.error(request, 'Invalid Credentials!')
		return redirect(reverse('login'))

	#return HttpResponse('In login submit')


def show_register(request):

	return render(request, "main/front/register.html", {})

def post_register(request):
	
	if request.method == "POST":

		name 		     = request.POST.get("name")
		username 		 = request.POST.get("username")
		email    		 = request.POST.get("email")
		password 		 = request.POST.get("password")
		confirm_password = request.POST.get("confirm_password")


		# Custom Validation
		Error_dict = {}

		if name == "":
			Error_dict.update({'name': "Name field required"})

		if username == "":
			Error_dict.update({'username': "Username field required"})


		if email == "":
			Error_dict.update({'email': "Email field required"})


		if password == "":
			Error_dict.update({'password': "Password field required"})
		elif len(password) < 6:
			Error_dict.update({'password': "Minimum 6 digits required"})


		if confirm_password == "":
			Error_dict.update({'confirm_password': "Confirm password field required"})
		elif len(confirm_password) < 6:
			Error_dict.update({'confirm_password': "Minimum 6 digits required"})
		elif confirm_password != password:
			Error_dict.update({'confirm_password': "Should match with password field"})


		if len(Error_dict) != 0:
			return render(request, 'main/front/register.html',{'error':Error_dict})


		if len(User.objects.filter(email = email)) == 0 and len(User.objects.filter(username = username)) == 0:

			password = make_password(password)

			user = User.objects.create(email = email, username = username, password = password)

			manager = Manager(name=name, email=email, user_text=username)
			manager.save()

			messages.success(request, 'Registered successfully, You can login Now!')
			return redirect(reverse('login'))

		else:
			messages.error(request, 'User Already Exists')
			return redirect(reverse('register.show'))


	


# Front logout 
def mylogout(request):

	logout(request)
	return redirect(reverse('login'))

# Admin change password
def show_change_password(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	return render(request, 'main/back/change_password.html', {})

def post_change_password(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	if request.method == "POST":

		old_password     = request.POST.get("old_password")
		new_password     = request.POST.get("new_password")
		confirm_password = request.POST.get("confirm_password")

		# Custom Validation
		Error_dict = {}
		if old_password == "":
			Error_dict.update({'old_password': "Old password field required"})
		elif len(old_password) < 6:
			Error_dict.update({'old_password': "Minimum 6 digits required"})

		if new_password == "":
			Error_dict.update({'new_password': "New password field required"})
		elif len(new_password) < 6:
			Error_dict.update({'new_password': "Minimum 6 digits required"})

		if confirm_password == "":
			Error_dict.update({'confirm_password': "Confirm password field required"})
		elif len(confirm_password) < 6:
			Error_dict.update({'confirm_password': "Minimum 6 digits required"})
		elif confirm_password != new_password:
			Error_dict.update({'confirm_password': "Should match with password field"})

		if len(Error_dict) != 0:
			return render(request, 'main/back/change_password.html',{'error': Error_dict})


		user = authenticate(username=request.user, password=old_password)

		if user != None :

			user = User.objects.get(username = request.user)
			user.set_password(new_password)
			user.save();

			messages.success(request, 'Password changed successfully')
			return redirect(reverse('changepassword.show'))

		else:
			messages.error(request, 'Incorrect old password')
			return redirect(reverse('changepassword.show'))






# Admin setting
def site_setting(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group 
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error}) 

	site_data = Main.objects.get(pk=1)

	return render(request, 'main/back/site_setting.html', {'site_data': site_data} )


# Admin, storing site setting 
def store_site_setting(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group 
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error}) 

	if request.method == "POST":

		name         = request.POST.get('name')
		site_phone   = request.POST.get('site_phone')
		facebook_link= request.POST.get('facebook_link')
		twitter_link = request.POST.get('twitter_link')
		youtube_link = request.POST.get('youtube_link')
		link         = request.POST.get('link')
		about        = request.POST.get('about')
		sitelogo     = request.POST.get('sitelogo')

		if facebook_link == "" : facebook_link = "#"
		if twitter_link  == "" : twitter_link = "#"
		if youtube_link  == "" : youtube_link = "#"
		if link          == "" : link = "#"


		# Custom Validation
		Error_dict = {}
		if name == "":
			Error_dict.update({'name': "Site Title field required"})
		if site_phone == "":
			Error_dict.update({'site_phone': "Site Contact field required"})
		if about == "":
			Error_dict.update({'about': "About field required"})

		if len(Error_dict) != 0:
			site_data = Main.objects.get(pk=1)
			return render(request, 'main/back/site_setting.html',{'error':Error_dict, 'site_data':site_data})


		sitelogo = request.FILES['sitelogo'] if 'sitelogo' in request.FILES else None
		file = ''
		fileurl = ''
		if sitelogo:

			if sitelogo.size > 5000000:

				Error_dict.update({'sitelogo': "Your file is bigger than 5 MB"})
				site_data = Main.objects.get(pk=1)
				return render(request, 'main/back/site_setting.html',{'error':Error_dict, 'site_data':site_data})


			if str(sitelogo.content_type).startswith('image'):
			 
				# create a new instance of FileSystemStorage
					fs = FileSystemStorage()
				# save attatched file
					file = fs.save(sitelogo.name, sitelogo)
				# The fileurl variable now contains the url to the file. This can be used to serve the file when needed.
					fileurl = fs.url(file)

			else:

				Error_dict.update({'sitelogo': "Site Logo format not supported"})
				site_data = Main.objects.get(pk=1)
				return render(request, 'main/back/site_setting.html',{'error':Error_dict, 'site_data':site_data})

		# Saving to database
		site_data 			= Main.objects.get(pk=1)
		site_data.name      = name
		site_data.tell      = site_phone
		site_data.fb        = facebook_link
		site_data.tw        = twitter_link
		site_data.yt        = youtube_link
		site_data.link      = link
		site_data.about     = about
		if file != "":
			site_data.picname   = file
			site_data.picurl    = fileurl

		site_data.save()

		messages.success(request, 'Site Data Updated Successfully')
		site_data = Main.objects.get(pk=1)
		return redirect(reverse('site_setting'))


# Show about setting 
def about_setting(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group 
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error}) 

	site_data = Main.objects.get(pk=1)
	return render(request, 'main/back/about_setting.html' ,{'site_data':site_data} )

# Admin, storing about setting 
def store_about_setting(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group 
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error}) 

	site_data = Main.objects.get(pk=1)

	if request.method == "POST":

		about = request.POST.get('about')


		# Custom Validation
		Error_dict = {}
		if about == "":
			Error_dict.update({'about': "About Title field required"})

		if len(Error_dict) != 0:
			site_data = Main.objects.get(pk=1)
			return render(request, 'main/back/about_setting.html',{'error':Error_dict, 'site_data':site_data})

		
		# Saving to database
		site_data 			= Main.objects.get(pk=1)
		site_data.about     = about
		site_data.save()

		messages.success(request, 'About Field Updated Successfully')
		return render(request, 'main/back/about_setting.html' ,{'site_data':site_data} )




def panel(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	return render(request, 'main/back/home.html')


