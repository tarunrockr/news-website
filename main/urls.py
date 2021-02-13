from django.urls import path
from .import views

urlpatterns = [
	
	path( '', views.home, name='home' ),
	path( 'about/',      		 views.about,         name='about' ),
	path( 'panel/',      		 views.panel,         name='panel' ),
	path( 'login/',      		 views.show_login,    name='login' ),
	path( 'login_post/', 		 views.login_submit,  name='login_post' ),
	path( 'register/',      	 views.show_register, name='register.show' ),
	path( 'register/post',       views.post_register, name='register.post' ),
	path( 'logout/',     		 views.mylogout,      name='logout' ),
	path( 'panel/setting/', 	 views.site_setting,  name='site_setting' ),
	path( 'panel/setting/store', views.store_site_setting,  name='site_setting.store' ),
	path( 'panel/aboutsetting/', views.about_setting, name='about_setting' ),
	path( 'panel/aboutsetting/store', views.store_about_setting, name='about_setting.store' ),
	path( 'panel/changepassword/show', views.show_change_password, name='changepassword.show' ),
	path( 'panel/changepassword/post', views.post_change_password, name='changepassword.post' ),
	path( 'contact/',     		 views.show_contact,      name='contact' ),
]