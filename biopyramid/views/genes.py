"""
This view runs all the relevant code for the "Genes" page, which displays a list of matching
genes after a search has been done.
"""
from pyramid.view import view_config

from genedataset import geneset

@view_config(route_name='/genes', renderer='biopyramid:templates/genes.mako')
def showPage(request):
	"""Show the page when the URL is called.
	"""
	if 'geneset' in request.session:	# restore previous list of genes
		gs = request.session['geneset']
		genes = []
		for item in gs.dataframe().reset_index().to_dict(orient="records"):  # won't return TranscriptLengths
			genes.append(dict([(key,val) for key,val in item.items() if key!="TranscriptLengths"]))
		name = gs.name
	else:
		genes = []
		name = None
	return {'genes':genes, 'name':name}

@view_config(route_name='/gene_search', renderer='json')
def geneSearch(request):
	"""Return a list of gene attributes given a search string.
	"""
	searchString = 	request.params.get('searchTerm')
	gs = geneset.Geneset().subset([searchString])
	if gs.size()>0:
		gs.name = searchString
		request.session['geneset'] = gs
	return gs.to_json()
