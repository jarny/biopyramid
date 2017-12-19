import unittest

from pyramid import testing

class DatasetsTest(unittest.TestCase):
	def setUp(self):
		self.config = testing.setUp()
		self.request = testing.DummyRequest()
		self.request.registry.settings['biopyramid.model.datadir'] = 'data'

	def tearDown(self):
		testing.tearDown()

	def test_datasteFiles(self):
		from .views import datasets
		request = self.request
		result = datasets.datasetFiles(request)
		#print 'sampleIds', result['sampleIds'][21]