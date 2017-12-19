"""
This view runs all the relevant code for the "About" page, which acts as the home page.
"""
from pyramid.view import view_config
	
@view_config(route_name='/about', renderer='biopyramid:templates/home.mako')
def home(request):
	"""Home page.
	"""
	return {}
	