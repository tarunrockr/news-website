import datetime
from main.models import Menu


def current_year_context_processor(request):

	current_datetime = datetime.datetime.now()

	return {
		'current_year':  current_datetime.year,
		'current_month': current_datetime.month,
		'current_day':   current_datetime.day
	}

def get_menu(request):

	menu_list = Menu.objects.all()

	return {
		'menu_list': menu_list
	}

