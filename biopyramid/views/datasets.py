"""
This view runs all the relevant code for the "Datasets" page, which displays a list of datasets.
"""
from pyramid.view import view_config

import os, json
from biopyramid.models import bpdataset

###########################################
# Utility methods - not mapped to URL
###########################################

def datasetFiles(request):
	"""
	Return a list all dataset files in the datasets directory, by looking for files ending
	with .h5 suffix. eg. ['/Users/jarnyc/BioPyramid/data/datasets/lanner.1.0.h5']
	"""
	# This is the dataset directory, set by the config file
	datadir = request.registry.settings['biopyramid.model.datadir']
	
	# Go through each file in the directory and fetch files with .h5 suffix
	filepaths = []
	for filename in os.listdir(datadir):
		if filename.endswith(".h5"):
			filepaths.append(os.path.join(datadir, filename))
	return filepaths
	
def datasetAttributes(request):
	"""
	Return a list of dictionaries, where each dictionary contains the attributes of the dataset.
	"filepath" key is also added to the final dictionary, so that it can be used to instantiate a BPDataset instance.
	"""
	return [bpdataset.datasetAttributes(filepath, includeFilepath=True) for filepath in datasetFiles(request)]

def datasetFromName(request, name):
	"""
	Return BPDataset instance based on name. Returns None if there is no matching dataset with the name.
	"""
	for attribute in datasetAttributes(request):
		if attribute['name']==name:
			return bpdataset.BPDataset(attribute['filepath'])
	return None


###########################################
# Methods that can be called by URL
###########################################

@view_config(route_name='/datasets', renderer='biopyramid:templates/datasets.mako')
def showPage(request):
	"""Shw the page when the URL is called.
	Provide a list of datasets in json format.
	"""
	return {'datasets':datasetAttributes(request)}
