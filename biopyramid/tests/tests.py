import unittest

from pyramid import testing

class ViewTests(unittest.TestCase):
	def setUp(self):
		self.config = testing.setUp()
		self.request = testing.DummyRequest()
		self.request.registry.settings['biopyramid.model.datadir'] = 'data'

	def tearDown(self):
		testing.tearDown()

	def test_home(self):
		from .views import home
		request = self.request
		#result = main(request)
		#print 'sampleIds', result['sampleIds'][21]