"""
This view runs all the relevant code for the "Expression" page, which plots the expression profile of a gene.
"""
from pyramid.view import view_config

from genedataset import geneset
from biopyramid.views import datasets
import numpy

@view_config(route_name='/expression', renderer='biopyramid:templates/expression.mako')
def showPage(request):
	"""Show the page when the URL is called.
	"""
	# Supply names of all datasets available for user to chooose from
	datasetNames = [item['name'] for item in datasets.datasetAttributes(request)]

	# Fetch BPDataset instance based on request parameter
	selectedDatasetName = request.params.get("dataset")
	if selectedDatasetName not in datasetNames:
		selectedDatasetName = datasetNames[0]
	dataset = datasets.datasetFromName(request, selectedDatasetName)

	# Fetch other required properties of the dataset
	sampleIds = dataset.sampleIds()
	sampleGroups = dataset.sampleGroups(returnType="display")
	sampleGroupItems = dict([(item, dataset.sampleGroupItems(sampleGroup=item)) for item in sampleGroups])
	sampleIdsAsGroupItems = dict([(group, dataset.sampleGroupItems(sampleGroup=group, duplicates=True)) for group in sampleGroups])

	# Fetch expression values of selected gene
	geneId = request.params.get("geneId")
	df = dataset.expressionMatrix(featureIds=[geneId])
	if len(df)==1:	# found a unique match for the gene
		expressionValues = numpy.log2(df[sampleIds]+1).to_dict(orient="split")['data'][0]
	else:	# either no match or multiple matches
		expressionValues = []

	return {'datasetNames':datasetNames, 
			'selectedDatasetName':selectedDatasetName, 
			'geneId':geneId,
			'expressionValues':expressionValues, 
			'sampleIds':sampleIds,
			'sampleGroups':sampleGroups, 
			'sampleGroupItems':sampleGroupItems, 
			'sampleIdsAsGroupItems':sampleIdsAsGroupItems}
