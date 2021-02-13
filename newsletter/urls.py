from django.urls import path 
from .import views

urlpatterns = [
	
	path('newsletter/add/', views.news_letter, name='newsletter'),

	#Admin routes
	path('panel/newsletter/emails/', views.news_letter_email, name='newsletteremail'),
	path('panel/newsletter/phones/', views.news_letter_phone, name='newsletterphone'),
	path('panel/newsletter/delete/<int:id>/<int:status>/', views.news_letter_delete, name='newsletterdelete'),
]