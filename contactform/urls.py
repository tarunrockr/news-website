from django.urls import path
from .import views

urlpatterns = [

	path( 'contact_submit/', views.contact_add,  name='contact.submit' ),
	# Admin functions
	path( 'contact_list/',    views.contact_list,     name='contact.list' ),
	path( 'contact_destroy/<int:id>', views.destroy_contact,  name='contact.destroy' ),
]