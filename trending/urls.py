from django.urls import path
from .import views

urlpatterns = [

	# Admin urls
	path('panel/trending/create', 				views.create_trending,   name='trending.create'),
	path('panel/trending/store',  				views.store_trending,    name='trending.store'),
	path('panel/trending/edit/<int:id>',        views.edit_trending,     name='trending.edit'),
	path('panel/trending/update/<int:id>',      views.update_trending,   name='trending.update'),
	path('panel/trending/delete/<int:id>',      views.trending_delete,   name='trending.delete'),

]