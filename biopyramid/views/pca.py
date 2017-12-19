"""
This view runs all the relevant code for the "PCA" page, which performs a PCA plot on a dataset.
"""
from pyramid.view import view_config

# This page uses some of the functions defined in datasets.py
from biopyramid.views import datasets

@view_config(route_name='/pca', renderer='biopyramid:templates/pca.mako')
def showPage(request):
	"""Show the PCA page, which has a list of available datasets so that user can plot PCA for 
	a different dataset after loading the page. The dataset can be selected by passing a parameter
	(eg. pca?dataset=lanner), otherwise the first dataset from the list will be selected.
	"""
	# Supply names of all datasets available for user to chooose from
	datasetNames = [item['name'] for item in datasets.datasetAttributes(request)]
	
	# Fetch BPDataset instance based on request parameter
	selectedDatasetName = request.params.get("dataset")
	if selectedDatasetName not in datasetNames:
		selectedDatasetName = datasetNames[0]
	dataset = datasets.datasetFromName(request, selectedDatasetName)
	
	# Fetch required properties. Note that pca coordinates have been saved already in the BPDataset instance for
	# quick retrieval. coords should be in 2xN shape, where N is the number of samples in the dataset.
	coords = dataset.pca.values.T[:2].tolist()
	sampleIds = dataset.sampleIds()
	sampleGroups = dataset.sampleGroups(returnType="display")
	sampleGroupItems = dict([(item, dataset.sampleGroupItems(sampleGroup=item)) for item in sampleGroups])
	sampleIdsAsGroupItems = dict([(group, dataset.sampleGroupItems(sampleGroup=group, duplicates=True)) for group in sampleGroups])
	
	return {'datasetNames':datasetNames, 
			'selectedDatasetName':selectedDatasetName, 
			'coords':coords, 
			'sampleIds':sampleIds,
			'sampleGroups':sampleGroups, 
			'sampleGroupItems':sampleGroupItems, 
			'sampleIdsAsGroupItems':sampleIdsAsGroupItems}

