<%
'''
Required inputs
datasets: list of dictionaries, each is the attributes of a dataset, such as name and description. eg:
		  [{'description': 'Single-Cell RNA-Seq Reveals Lineage and X Chromosome Dynamics in Human Preimplantation Embryos', 
			'fullname': 'Lanner', 
			'name': 'lanner', 
			'pubmed_id': '27062923', 
			'species': 'HomoSapiens', 
			'version': '1.0'}]
'''
import json
%>

<%namespace name="common_elements" file="common.mako"/>

<!doctype html>
<html lang="en">
<head>
	<!-- Load html containing menu, which is the same for all pages -->
	${common_elements.header_elements()}

	<script>
	// It's easier for long term maintenance if python variables are first mapped to javascript variables in the one place
	var tableData = ${json.dumps(datasets) | n};
	</script>
</head>

<body>
	${common_elements.banner()}
	<div class="content">
		<div class="container">
			<div class="main">
				<h1>Datasets</h1>
				<p>This page shows all the datasets which have been uploaded into your application.</p>
				<div style="margin-top:50px;">
				<table>
					<thead>
						<th>name</th>
						<th>fullname</th>
						<th>description</th>
						<th>pubmed_id</th>
						<th>species</th>
						<th>version</th>
					</thead>

					<tbody>
						<tr v-for='row in rows'>
						  <td>{{ row.name }}</td>
						  <td>{{ row.fullname }}</td>
						  <td>{{ row.description }}</td>
						  <td>{{ row.pubmed_id }}</td>
						  <td>{{ row.species }}</td>
						  <td>{{ row.version }}</td>
						</tr>
					</tbody>
				</table>
				</div>
			</div>
			
			<div class="aside">
			<h4>Information about this page</h4>
			<ul>
			<li>views/datasets.py contains all methods relevant to this page.</li>
			<li>templates/datasets.mako contains the html that renders this page.</li>
			<li>Uses the data directory specified in the config file (.ini file) to 
			determine where the dataset files reside.</li>
			<li>Relies on models/bpdataset.py to fetch details about datasets.</li>
			</ul>
			</div>
		</div>
	</div>
	${common_elements.footer()}

	<script>
	var vm = new Vue({
		el: '.content',
		data: {
			rows: tableData
		},
		methods: {
		}
	})
	</script>

</body>
</html>
