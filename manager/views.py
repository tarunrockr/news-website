from  django.shortcuts import render, get_object_or_404, redirect 
from .models import Manager
from  news.models import News
from  category.models import Category
from  subcategory.models import SubCategory
from  django.db import connection
from  django.http import HttpResponse 
from  django.urls import reverse
from  django.contrib.auth import authenticate, login, logout
from  django.core.files.storage import FileSystemStorage
from  django.contrib import messages
from  trending.models import Trending
import random
from random import randint
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType

# Create your views here.

def userlist(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group 
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error}) 

	manager_list = Manager.objects.all()

	return render(request, 'manager/back/userlist.html', {'manager_list':manager_list})

def delete_user(request, id):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group 
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error}) 

	try:

		manager = Manager.objects.get(pk=id);

		# Deleting the user related to this manager
		user = User.objects.get(username = manager.user_text);
		user.delete()

		manager.delete();

		messages.success(request, 'Manager Deleted Successfully.')
		return redirect(reverse('manager.userlist'))

	except:

		messages.error(request, 'Error occured')
		return redirect(reverse('manager.userlist'))


# Creating the group list 
def manager_group(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group 
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error}) 

	group = Group.objects.all().exclude(name='masteruser')

	return render(request, 'manager/back/manager_group.html', {'group_list': group})

# Adding the group
def store_group(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group 
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error}) 

	try:
		if request.method == "POST":

			name = request.POST.get('name')


			# Custom Validation
			Error_dict = {}
			if name == "":
				Error_dict.update({'name': "Name field required"})

			if len(Error_dict) != 0:
				group = Group.objects.all()
				return render(request, 'manager/back/manager_group.html', {'group_list': group, 'error':Error_dict})

			if len(Group.objects.filter(name=name)) != 0:
				Error_dict.update({'name': "Name already exists"})
				group = Group.objects.all()
				return render(request, 'manager/back/manager_group.html', {'group_list': group, 'error':Error_dict})

			# Adding to database
			group = Group(name=name)
			group.save()

			messages.success(request, 'Group added successfully!')
			return redirect(reverse('manager.group'))
	except:
		messages.error(request, "Error occured")
		return redirect(reverse('manager.group'))


# Delete group
def destroy_group(request, id):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group 
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error}) 

	try:
		group = Group.objects.filter(pk=id)
		group.delete()

		messages.success(request, "Group deleted Successfully")
		return redirect(reverse('manager.group'))

	except:

		messages.error(request, "Error Occured")
		return redirect(reverse('manager.group'))


# Showing the group list assigned to user
def users_groups(request, manager_id):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group 
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error}) 

	manager = Manager.objects.get(id=manager_id)
	user = User.objects.get(username = manager.user_text)

	# Here we are getting the groups assigned to this user
	usergroup = []
	for grp in user.groups.all():
		usergroup.append(grp.name)

	group = Group.objects.all()

	#return HttpResponse("Manager ID: "+str(manager.name))

	return render(request, 'manager/back/users_groups.html', {'usergroup': usergroup, 'grouplist': group, 'manager':manager, 'user': user})

# Adding group to a user
def store_users_groups(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group 
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error}) 

	if request.method == "POST":

		try:

			user_id  	= request.POST.get('user_id')
			group_id 	= request.POST.get('group')
			manager_id 	= request.POST.get('manager_id')

			group = Group.objects.get(pk=group_id)
			user  = User.objects.get(pk=user_id)

			# Adding the group to the user
			user.groups.add(group)

			messages.success(request, "Group assigned successfully to user")
			return redirect(reverse('users_groups', kwargs={'manager_id': manager_id} ))

		except:

			messages.error(request, "Error Occured")
			return redirect(reverse('users_groups', kwargs={'manager_id': manager_id}))


# Remove group from a user
def remove_users_groups(request, manager_id, group_name):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group 
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error}) 

	try:

		manager = Manager.objects.get(pk=manager_id)
		group 	= Group.objects.get(name=group_name)
		user  	= User.objects.get(username=manager.user_text)

		# Remove the group to the user
		user.groups.remove(group)

		messages.success(request, "Group removed successfully to user")
		return redirect(reverse('users_groups', kwargs={'manager_id': manager_id} ))

	except:

		messages.error(request, "Error Occured")
		return redirect(reverse('users_groups', kwargs={'manager_id': manager_id}))


# Creating the permission list 
def manager_permission(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group 
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error}) 

	perms = Permission.objects.all()

	return render(request, 'manager/back/manager_permission.html', {'permission_list': perms})



# Delete permission
def destroy_permission(request, id):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group 
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error}) 

	try:
		permission = Permission.objects.filter(pk=id)
		permission.delete()

		messages.success(request, "Permission deleted Successfully")
		return redirect(reverse('manager.permission'))

	except:

		messages.error(request, "Error Occured")
		return redirect(reverse('manager.permission'))


# Adding the group
def store_permission(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group 
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error}) 

	try:
		if request.method == "POST":

			name 	 = request.POST.get('name')
			codename = request.POST.get('codename')
			# return HttpResponse(name)

			# Custom Validation
			Error_dict = {}
			if name == "":
				Error_dict.update({'name': "Name field required"})
			if codename == "":
				Error_dict.update({'codename': "Codename field required"})

			if len(Error_dict) != 0:
				permission = Permission.objects.all()
				return render(request, 'manager/back/manager_permission.html', {'permission_list': permission, 'error':Error_dict})

			if len(Permission.objects.filter(codename=codename)) != 0:
				# return HttpResponse("jhgjhgj")
				Error_dict.update({'codename': "Codename already exists"})
				permission = Permission.objects.all()
				return render(request, 'manager/back/manager_permission.html', {'permission_list': permission, 'error':Error_dict})

			# Adding permission to database
			content_type = ContentType.objects.get(app_label='main', model='main')
			permi   = Permission.objects.create(codename=codename, name=name, content_type=content_type) 

			messages.success(request, 'Permission added successfully!')
			return redirect(reverse('manager.permission'))
	except:
		messages.error(request, "Error occured")
		return redirect(reverse('manager.permission'))
		


# Showing the permission list assigned to sprecific user (Specific permission to a user)
def users_permissions(request, manager_id):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group 
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error}) 

	manager = Manager.objects.get(id=manager_id)
	user = User.objects.get(username = manager.user_text)

	permiss = Permission.objects.filter(user=user)

	# Here we are getting the groups assigned to this user
	userpermissions = []
	for per in permiss:
		userpermissions.append(per.name)

	permission_list = Permission.objects.all()

	#return HttpResponse("Manager ID: "+str(manager.name))

	return render(request, 'manager/back/users_permissions.html', {'userpermissions': userpermissions, 'permission_list': permission_list, 'manager':manager, 'user': user})


# Assign permission to a user (specific permission)
def store_users_permissions(request):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group , START
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error})
	# Allow this section to only masteruser group , END 

	if request.method == "POST":

		try:

			user_id  		= request.POST.get('user_id')
			permission_id 	= request.POST.get('permission')
			manager_id 		= request.POST.get('manager_id')

			permission = Permission.objects.get(pk=permission_id)
			user  	   = User.objects.get(pk=user_id)

			# Adding the permission to the user (specific permission)
			user.user_permissions.add(permission)

			messages.success(request, "Permission assigned successfully to user")
			return redirect(reverse('users_permissions', kwargs={'manager_id': manager_id} ))

		except:

			messages.error(request, "Error Occured")
			return redirect(reverse('users_permissions', kwargs={'manager_id': manager_id}))


# Remove permission from a user (specific permission)
def remove_users_permissions(request, manager_id, permission_name):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group , START
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error})
	# Allow this section to only masteruser group , END 

	try:

		manager 	= Manager.objects.get(pk=manager_id)
		permission 	= Permission.objects.get(name=permission_name)
		user  		= User.objects.get(username=manager.user_text)

		# Remove the permission to the user (specific permission)
		user.user_permissions.remove(permission)

		messages.success(request, "Permission removed successfully from user")
		return redirect(reverse('users_permissions', kwargs={'manager_id': manager_id} ))

	except:

		messages.error(request, "Error Occured")
		return redirect(reverse('users_permissions', kwargs={'manager_id': manager_id}))


# Showing the permission list assigned to groups
def groups_permissions(request, group_id):

	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group 
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error}) 

	# manager = Manager.objects.get(id=manager_id)
	# user    = User.objects.get(username = manager.user_text)

	# Here we are getting the permissions assigned to this group
	# usergroup = []
	# for grp in user.groups.all():
	# 	usergroup.append(grp.name)

	group 		 = Group.objects.get(pk=group_id)
	groups_perms = group.permissions.all()

	permission_list   = Permission.objects.all()

	#return HttpResponse("Manager ID: "+str(manager.name))group_id

	return render(request, 'manager/back/groups_permissions.html', {'groups_perms': groups_perms, 'permission_list': permission_list,'group': group})


# Assigning the permissions to group
def store_groups_permissions(request):
	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group , START
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error})
	# Allow this section to only masteruser group , END 

	if request.method == "POST":

		try:

			group_id  		= request.POST.get('group_id')
			permission_id 	= request.POST.get('permission')

			permission = Permission.objects.get(pk=permission_id)
			group      = Group.objects.get(pk=group_id)

			# Adding the permission to the group
			group.permissions.add(permission)

			messages.success(request, "Permission assigned successfully to Group")
			return redirect(reverse('groups_permissions', kwargs={'group_id': group_id} ))

		except:


			messages.error(request, "Error Occured")
			return redirect(reverse('groups_permissions', kwargs={'group_id': group_id}))


# Remove permission from a group
def remove_groups_permisions(request, group_id, permission_id):
	#return HttpResponse(permission_id)
	# Login check START
	if not request.user.is_authenticated :
		return redirect(reverse('login'))
	# Login check END

	# Allow this section to only masteruser group , START
	perm = 0
	for i in request.user.groups.all():
		if i.name == 'masteruser': perm = 1

	if perm == 0:
		error ="Access Denied!"
		return render(request, "error/error.html", {'error': error})
	# Allow this section to only masteruser group , END 

	try:
		group 	    = Group.objects.get(pk=group_id)
		permission 	= Permission.objects.get(pk=permission_id)


		# Remove the permission from the group
		group.permissions.remove(permission)

		messages.success(request, "Permission removed successfully from group")
		return redirect(reverse('groups_permissions', kwargs={'group_id': group_id} ))

	except:

		messages.error(request, "Error Occured")
		return redirect(reverse('groups_permissions', kwargs={'group_id': group_id}))


