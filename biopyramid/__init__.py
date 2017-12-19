from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
#from views.views import RootFactory


def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	session_factory = session_factory_from_settings(settings)

	config = Configurator(settings=settings)
	config.set_session_factory(session_factory)

	config.include('pyramid_mako')

	config.add_static_view('static', 'static', cache_max_age=3600)
	config.add_static_view('css', 'static/css')
	config.add_static_view('images', 'static/images')
	config.add_static_view('js', 'static/js')

	config.add_route('/about', '/')
	
	config.add_route('/genes', '/genes')
	config.add_route('/gene_search','/gene_search')
	
	config.add_route('/datasets', '/datasets')
	
	config.add_route('/pca', '/pca')	
	config.add_route('/expression', '/expression')
	
	config.scan()
	return config.make_wsgi_app()
