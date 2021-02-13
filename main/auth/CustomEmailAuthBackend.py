from django.contrib.auth.models import User 

class EmailAuthBackend:

	def authenticate(self, request, username, password):

		try:	
			user = User.objects.get(email=username)
			success = user.check_password(password)
			if(success):
				return user

		except User.DoesNotExists:
			pass

		return None

	def get_user(self, uid):
		try:
			return User.objects.get(pk=uid)
		except:
			return None





# from django.contrib.auth import get_user_model
# from django.contrib.auth.backends import ModelBackend

# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         UserModel = get_user_model()
#         try:
#             user = UserModel.objects.get(email=username)
#         except UserModel.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password):
#                 return user
#         return None
