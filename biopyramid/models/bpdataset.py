"""
This module extends genedataset.dataset by providing extra data and functionality. These extra data
can be specific to the BioPyramid application, such as colours or ordering used for sample groups.

Note on mutex:
At one stage, the HDF file created by the dataset had issues when multiple users were trying to access
the same dataset at exactly the same moment (it crashed the server!), even though the file was read only. 
Hence we came up with a way to "lock" the file briefly while one user accesses it through this 
mutual exclusion (mutex) system. Even though there have been updates to HDF packages since these issues 
(late 2016), we've kept the code here as a safeguard.
"""
import pandas
import genedataset.dataset
import biopyramid.views.mutex as mutex

def createDatasetFile(destDir, **kwargs):
	"""
	This function extends genedataset.dataset.createDatasetFile() by adding more objects to the .h5
	file created, as these objects are used by BioPyramid.

	Parameters
	----------
	The same parameters as genedataset.dataset.createDatasetFile() are needed. In addition we need:
	sampleGroupsDisplayed: (list) a subset list of sample groups used by BioPyramid for display, eg ['celltype', 'tissue']
		Any sample group not in this list will be used for descriptive purposes only and not used
		for selection in various parts of the application, including grouping samples for plots, for example.
	sampleGroupOrdering: (dict) of list keyed on sample group, for ordering of items within
		the sample group, eg: {'celltype':['T1','T2',...],...}
	sampleGroupColours: (dict) of colour values keyed on sample group and item, 
		eg: {'cell_lineage': {'Stem Cell':'#cccccc', ...}, ... }
	pca: (pandas.DataFrame) coordinates of PCA calculation to be stored. It should be in NxD shape, where
		N is the number of samples in the data and D is the number of dimensions used for pca.

	All parameters are optional and empty ones will be created if unspecified.
	"""
	sampleGroupsDisplayed = kwargs.get('sampleGroupsDisplayed', [])
	sampleGroupOrdering = kwargs.get('sampleGroupOrdering', {})
	sampleGroupColours = kwargs.get('sampleGroupColours', {})
	pca = kwargs.get('pca', pandas.DataFrame())
	ds = genedataset.dataset.createDatasetFile(destDir, **kwargs)
	
	instantiateDatasetFile(ds, sampleGroupsDisplayed, sampleGroupOrdering, sampleGroupColours, pca)		

	return BPDataset(ds.filepath)


@mutex.mutual_exclusion
def instantiateDatasetFile(ds, sampleGroupsDisplayed, sampleGroupOrdering, sampleGroupColours, pca):
	"""This function is used to 
	"""
	store = ds.hdfStore()
	store['/series/sampleGroupsDisplayed'] = pandas.Series(sampleGroupsDisplayed)
	store['/series/sampleGroupOrdering'] = pandas.Series(sampleGroupOrdering)
	store['/series/sampleGroupColours'] = pandas.Series(sampleGroupColours)
	store['/dataframe/pca'] = pca
	store.close()

	
def datasetAttributes(filepath, includeFilepath=False):
	"""
	Return a dictionary of dataset attributes from hdf5 file:
		(name, fullname, species, version, description, pubmed_id, parent)
	This is the same as attributes() method on the BPDataset instant, but should be
	faster since it only extracts the attributes rather than all other values.
	
	If includeFilepath is true, filepath is included in the dictionary, which is useful when trying
	to recover this info from afterwards
	"""
	import os
	if os.path.exists(filepath):
		
		attributes = mutex.hdf_attr_to_dict(filepath, '/series/attributes')
	
		if includeFilepath:
			attributes['filepath'] = filepath
		
		return attributes
	else:
		return {}
	
	
class BPDataset(genedataset.dataset.Dataset):
	"""
	Class to handle a dataset object. Inherits from genedataset.dataset.Dataset but has extra attributes
	more specific to BioPyramid such as sample group colours.
	
	Full list of keys and objects stored in the hdf file:
	
		/series/attributes: (name, fullname, species, version, description, pubmed_id, expression_data_keys)
		/series/sampleGroupsDisplayed
		/series/sampleGroupOrdering
		/series/sampleGroupColours
		/dataframe/samples
		/dataframe/expression/[expression_data_key]

	If attributes['expression_data_keys']=['counts','cpm'], for example, the hdf file will have
	'dataframe/expression/counts' and 'dataframe/expression/cpm' as keys.
	"""
	
	
	@mutex.mutual_exclusion
	def __init__(self, pathToHDF):
		"""Instantiate the object by reading the hdf file given by pathToHDF
		"""
		super(BPDataset, self).__init__(pathToHDF)
		
		self._sampleGroupColours = pandas.read_hdf(self.filepath, '/series/sampleGroupColours')
		self._sampleGroupOrdering = pandas.read_hdf(self.filepath, '/series/sampleGroupOrdering')
		self._sampleGroupsDisplayed = pandas.read_hdf(self.filepath, '/series/sampleGroupsDisplayed')
		self.pca = pandas.read_hdf(self.filepath, '/dataframe/pca')
				
	def sampleGroups(self, returnType=None):
		"""
		Return a list of sample group names eg: ["celltype","tissue"]. Override base class method
		in order to ensure correct ordering and filtering.

		Parameters
		----------
		returnType: {None, "display"}. If display, it returns only sample groups defined as for display.
		This is useful when not all sample groups are important for data aggregation or differential expression.
		
		Returns
		----------
		a list
		"""
		if returnType=="display":
			return self._sampleGroupsDisplayed.tolist()
		else:
			return super(BPDataset, self).sampleGroups()
				
	def sampleGroupItems(self, sampleGroup=None, groupBy=None, duplicates=False):
		"""
		Return sample group items belonging to sampleGroup, eg: ["B1","B2"]. Override base class method
		to enforce correct ordering.
		
		Parameters
		----------
		sampleGroup: name of sample group, eg: 'celltype'
		groupBy: name of another sample group for grouping, eg: 'cell_lineage'
		duplicates: boolean to return a list of unique values in the list avoiding duplicates if False; 
			if True, it specifies a list of sample group items in the same order/position as columns of 
			expression matrix; ignored if groupBy is specified.
		
		Returns
		----------
		list if groupBy is None, eg: ['B1','B2',...]. If duplicates is True, the list
			returned is the same length as dataset's columns in its expression matrix, and in the same
			corresponding position.
		dictionary of list if groupBy is specified, eg: {'Stem Cell':['LSK','STHSC',...], ...}
			groupBy sorts the flat list which would have been returned without groupBy into
			appropriate groups.
			
		Note that this method does not make assumptions about the integrity of the data returned for 
		groupBy specification. So it's possible to return {'Stem Cell':['LSK','STHSC'], 'B Cells':['LSK','B1']},
		if there is a sample id which has been assigned to ('LSK','Stem Cell') and another to ('LSK','B Cells') by mistake.
		"""
		df = self.samples
		sgo = self._sampleGroupOrdering
		
		if sampleGroup in df.columns and groupBy in df.columns: # group each item by sample ids, then substitute items from sampleGroup
			sampleIdsFromGroupBy = dict([(item, df[df[groupBy]==item].index.tolist()) for item in set(df[groupBy])])
			# {'Stem Cell':['sample1','sample2',...], ... }
		
			# substitute items from sampleGroup for each sample id
			dictToReturn = {}
			for sampleGroupItem in sampleIdsFromGroupBy.keys():
				# this is the set of matching sample group items with duplicates removed, eg: set(['LSK','CMP',...])
				groupItems = set([df.at[sampleId,sampleGroup] for sampleId in sampleIdsFromGroupBy[sampleGroupItem]])
				# order by sgo
				if sampleGroup in sgo:
					indexedItems = [(sgo[sampleGroup].index(item) if item in sgo[sampleGroup] else None, item) for item in groupItems]
					dictToReturn[sampleGroupItem] = [value[1] for value in sorted([item for item in indexedItems if item[0] is not None])] + [item[1] for item in indexedItems if item[0] is None]
				else:
					dictToReturn[sampleGroupItem] = sorted(groupItems)
			return dictToReturn
		
		elif sampleGroup in df.columns:
			if duplicates:
				return super(BPDataset, self).sampleGroupItems(sampleGroup=sampleGroup, duplicates=True)
				
			groupItems = set(df[sampleGroup])
			# order them if possible
			if sampleGroup in sgo:
				indexedItems = [(sgo[sampleGroup].index(item) \
								 if item in sgo[sampleGroup] else None, item) for item in groupItems if pandas.notnull(item)]
				return [value[1] for value in sorted([item for item in indexedItems if item[0] is not None])] + \
						[item[1] for item in indexedItems if item[0] is None]
			else:
				return sorted([item for item in groupItems if pandas.notnull(item)])

		else:
			return []
			
	def sampleGroupColours(self, sampleGroup=None):
		"""Return colour dictionary given sampleGroup, eg: {'Stem Cell':'#cccccc', ...}
		If sampleGroup==None, returns the dictionary with enclosing sample groups as keys, 
		eg: {'cell_lineage': {'Stem Cell':'#cccccc', ...}, ...}
		
		Parameters:
			sampleGroup: string, a member of self.sampleGroups()
			
		"""
		series = self._sampleGroupColours

		if sampleGroup:
			return series[sampleGroup] if sampleGroup in series else {}  # series[sampleGroup] is already a dict
		else:
			return series.to_dict()		
		
	def sampleGroupOrdering(self, sampleGroup=None):
		"""Return list of ordered sample group items given sampleGroup, eg: ['LSK','MPP', ...]
		If sampleGroup==None, returns the dictionary with enclosing sample groups as keys, 
		eg: {'celltype': ['LSK','MPP', ...], ...}
		
		Parameters:
			sampleGroup: string, a member of self.sampleGroups()
			
		"""
		series = self._sampleGroupOrdering
		if sampleGroup:
			return series[sampleGroup] if sampleGroup in series else {}  # series[sampleGroup] is already a dict
		else:
			return series.to_dict()

	def sampleTable(self):
		"""Ensure that 'sampleId' is always the name of the index, just in case it was left out.
		"""
		df = self.samples
		df.index.name = 'sampleId'
		return df
	