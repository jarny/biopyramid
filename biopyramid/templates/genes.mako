<%
'''
This mako template renders the Genes page, which shows a search field and a list of genes in a table after the search is done.

Required input:
genes: json version of a geneset.Geneset instance, ie. a list of dictionaries, eg:
	[{'GeneId':'ENSG00000183625', 
	  'GeneSymbol':'CCR3', 
	  'EntrezId':'1232', 
	  'Synonyms':'CC-CKR-3|CD193|CKR3|CMKBR3',
	  'Description':'C-C motif chemokine receptor 3'}, ...]
name: (string) geneset.Geneset name, which is the same as the last term used for search
'''
import json
%>

<%namespace name="common_elements" file="common.mako"/>

<!doctype html>
<html lang="en">
<head>
	<!-- Load html containing header elements, which are the same for all pages -->
	${common_elements.header_elements()}

	<!-- This javascript library is used for ajax calls -->
	<script type="text/javascript" src="/js/axios.min.js"></script>

	<script>
	// Define all the variables which come from python. Even though it's possible to inject these variables anywhere
	// using the template variable syntax, mapping them all to one javascript variable here is recommended, 
	// as it makes it easier for long term maintenance.
	var dataFromPython =  {
		genes: ${json.dumps(genes) |n},
		name: ${json.dumps(name) |n}
	};

	var vm;	// This will be assigned to a Vue instance below. Having this as a global makes it easy to access it from console.
	</script>
</head>
<body>
	<!-- Load html containing menu, which is the same for all pages -->
	${common_elements.banner()}

	<div class="content">
		<div class="container">
			<div class="main">
				<h1>Genes</h1>
				<p>The user can search for a gene and see the matching entries as a table on this page.</p>
				<p>Search for a gene: <input type="text" v-model="searchTerm" @keyup.enter="search" placeholder="[example: Ccr3]">
					<button @click="search">search</button>
				</p>
				<div style="margin-top:50px;">
				<h3 v-show="lastSearchTerm!=null" style="text-align:center; margin-bottom:20px;">{{lastSearchTerm}} ({{tableRows.length}} entries)</h3>
				<table width="100%">
					<thead>
						<th>Ensembl Id</th>
						<th>Symbol</th>
						<th>Entrez Id</th>
						<th>Synonyms</th>
						<th>Description</th>
						<th>Expression</th>
					</thead>

					<tbody>
						<tr v-for='row in tableRows'>
						  <td><a v-bind:href="'http://www.ensembl.org/Gene/Summary?g=' + row.EnsemblId" target="_blank">{{ row.EnsemblId }}</a></td>
						  <td>{{ row.GeneSymbol }}</td>
						  <td><a v-bind:href="'http://www.ncbi.nlm.nih.gov/sites/entrez?db=gene&term=' + row.EntrezId" target="_blank">{{ row.EntrezId }}</a></td>
						  <td v-html="truncate(row.Synonyms, 10)"></td>
						  <td v-html="truncate(row.Description, 30)"></td>
						  <td><a v-bind:href="'/expression?geneId=' + row.EnsemblId">expression</a></td>
						</tr>
					</tbody>
				</table>
				</div>
			</div>
			
			<div class="aside">
			<h4>Information about this page</h4>
			<ul>
			<li>views/genes.py contains all methods relevant to this page.</li>
			<li>templates/genes.mako contains the html that renders this page.</li>
			<li>relies on <a href="https://github.com/jarny/genedataset" target="_blank">genedataset</a> package for looking up gene annotation.</li>
			</ul>
			</div>
		</div>
	</div>
	${common_elements.footer()}

	<script>
	// Define Vue instance, which handles all the interactions within the page.
	vm = new Vue({
		el: '.content',
		
		data: {	// define all variables used by the Vue instance
			searchTerm: null,	// bound to whatever user is entering as input string
			lastSearchTerm: dataFromPython.name,	// remember the last term used to show the table
			tableRows: dataFromPython.genes
		},

		methods: {	// define all methods used by the Vue instance
			// Some strings can be very long, so truncate them and add ellipsis 
			truncate : function(value, length) {
				if(value.length < length) {
					return value;
				}
				length = length - 3;
				return value.substring(0, length) + " <a href='#' title='" + value + "' style='text-decoration:none'>" + '...' + "</a>";
			},

			// Perform the search
	  		search: function() {
				axios.get('/gene_search', {
					params: {
						searchTerm: this.searchTerm
					}
				}).then(response => {
					var data = JSON.parse(response.data); // should be an array
					if (data.length==0) {
						alert("No matching genes found.");
						return;
					}
					this.tableRows = data;
					this.lastSearchTerm = this.searchTerm;
				});
	  		}
		}
	})
	</script>

</body>
</html>
