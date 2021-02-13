from django.urls import path
from .import views

urlpatterns = [
	
	# All users
	path( 'panel/manager/userlist',  views.userlist,  name='manager.userlist' ),
	path( 'panel/manager/delete/<int:id>/', views.delete_user, name='manager.delete' ),

	# All groups
	path( 'panel/group',  views.manager_group,  name='manager.group' ),
	path( 'panel/group/store',  views.store_group,  name='manager.group.store' ),
	path( 'panel/group/delete/<int:id>/', views.destroy_group, name='manager.group.delete' ),

	# Groups assigned to users
	path( 'panel/users_groups/<int:manager_id>/', views.users_groups, name="users_groups"),
	path( 'panel/users_groups/add', views.store_users_groups, name="users_groups.store"),
	path( 'panel/users_groups/delete/<int:manager_id>/<str:group_name>/', views.remove_users_groups, name="users_groups.delete"),

	# All permissions
	path( 'panel/permission',  views.manager_permission,  name='manager.permission' ),
	path( 'panel/permission/store',  views.store_permission,  name='manager.permission.store' ),
	path( 'panel/permission/delete/<int:id>/', views.destroy_permission, name='manager.permission.delete' ),

	# Users specific permission
	path( 'panel/users_permissions/<int:manager_id>/', views.users_permissions, name="users_permissions"),
	path( 'panel/users_permissions/add', views.store_users_permissions, name="users_permissions.store"),
	path( 'panel/users_permissions/delete/<int:manager_id>/<str:permission_name>/', views.remove_users_permissions, name="users_permissions.delete"),

	# Permissions assigned to Groups
	path( 'panel/groups_permissions/<int:group_id>', views.groups_permissions, name="groups_permissions"),
	path( 'panel/groups_permissions/store',  views.store_groups_permissions,  name='groups_permissions.store' ),
	path( 'panel/groups_permissions/delete/<int:group_id>/<int:permission_id>/', views.remove_groups_permisions, name="groups_permissions.delete"),
]