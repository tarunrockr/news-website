from django.shortcuts import render, get_object_or_404, redirect 
from .models import Newsletter
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


def news_letter(request):

	if request.method == "POST":

		emailorphone = request.POST.get('newsletter_txt')

		news_letter_obj = Newsletter()

		result = emailorphone.find('@')

		if int(result) != -1:
			# it is email
			news_letter_obj.emailorphone = emailorphone
			news_letter_obj.status = 1
			news_letter_obj.save()
		else:
			try:

				# it is number
				news_letter_obj.emailorphone = int(emailorphone)
				news_letter_obj.status = 1
				news_letter_obj.save()
			except:
				return redirect(reverse('home'))

	return redirect(reverse('home'))


#Admin urls
# Show email list of newsletter
def news_letter_email(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	email_list = Newsletter.objects.filter(status=1)

	return render(request, 'newsletter/back/emails.html', {'email_list': email_list})


# Show email list of newsletter
def news_letter_phone(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	phone_list = Newsletter.objects.filter(status=2)

	return render(request, 'newsletter/back/phones.html', {'phone_list': phone_list})

# SDelete newsletter
def news_letter_delete(request, id, status):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	newsletter = Newsletter.objects.get(pk=id)
	newsletter.delete()

	messages.warning(request, 'Newsletter deleted successfully')

	if status==1:	
		return redirect(reverse('newsletteremail'))
	else:
		return redirect(reverse('newsletterphone'))











