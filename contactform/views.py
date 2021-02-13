from  django.shortcuts import render, get_object_or_404, redirect 
from .models import ContactForm
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




def contact_add(request):

	if request.method == "POST":

		name     = request.POST.get('name')
		email    = request.POST.get('email')
		message  = request.POST.get('message')

		# Custom Validation
		Error_dict = {}
		if name == "":
			Error_dict.update({'name': "Name field required"})

		if email == "":
			Error_dict.update({'email': "Email field required"})

		if message == "":
			Error_dict.update({'message': "Message field required"})

		if len(Error_dict) != 0:
			return render(request, 'main/front/contact.html',{'error':Error_dict})

		# Saving contact form
		contact = ContactForm( name = name, email = email , message = message, date =  datetime.now() )
		contact.save()

		messages.success(request, 'Thank you for contacting us')
		return render(request, 'main/front/contact.html', {})

# Admin side function to show contact list
def contact_list(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	contact_list = ContactForm.objects.all()

	return render(request, 'main/back/contact_list.html', { 'contact_list': contact_list })

# Admin side function to delete contact message
def destroy_contact(request, id):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	try:

		contact = ContactForm.objects.get(pk=id)
		contact.delete()

		messages.success(request, 'Contact deleted successfully!')
		return render(request, 'main/back/contact_list.html', { 'contact_list': contact_list })
		
	except :

		messages.error(request, 'Error Occured!')
		return render(request, 'main/back/contact_list.html', { 'contact_list': contact_list })

	

