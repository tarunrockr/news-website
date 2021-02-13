from django.urls import path
from .import views

urlpatterns = [
	
	path('panel/category/list',  views.category_list,    name='category.list' ),
	path('panel/category/add',   views.create_category,  name='category.create' ),
	path('panel/category/store', views.store_category,   name='category.store' ),

]