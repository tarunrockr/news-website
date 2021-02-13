from django.urls import path
from .import views

urlpatterns = [
	
	path('panel/subcategory/list',  views.subcategory_list,    name='subcategory.list' ),
	path('panel/subcategory/add',   views.create_subcategory,  name='subcategory.create' ),
	path('panel/subcategory/store', views.store_subcategory,   name='subcategory.store' ),

]