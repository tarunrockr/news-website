from django.urls import path
from .import views

urlpatterns = [
	
	# path( '', views.home, name='home' ),
	path( 'news/<int:news_id>/', views.news_detail, name='news.detail' ),

	# Admin routes
	path( 'panel/news/list', 					views.news_list, name='news.list' ),
	path( 'panel/news/add', 					views.add_news, name='news.add' ),
	path( 'panel/news/store', 					views.store_news, name='news.store' ),
	path( 'panel/news/edit/<int:id>/', 			views.edit_news, name='news.edit' ),
	path( 'panel/news/update/<int:id>/', 		views.update_news, name='news.update' ),
	path( 'panel/news/destroy/<int:id>/', 	   	views.destroy, name='news.delete' ),
	path( 'panel/news/fetch_subcategory_ajax',  views.fetch_subcategory_ajax, name='news.fetch.subcategory'),
	path( 'panel/news/activeToggleAjax',        views.activation_toggle_ajax, name='news.toggleactivation'),
]