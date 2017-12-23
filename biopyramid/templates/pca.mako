<%
'''
Required inputs for this template, with examples:
	datasetNames: list of available dataset names, ['lanner',...]
	selectedDatasetName: selected name from list of available dataset names, 'lanner'
	coords: PCA coordinates as list of lists in Nx2 shape, [[2.1, 0.2, ...], [3.3, 0.0, ...]]
	sampleIds: list of sample ids in the same matching order as coords[0], ['sample1','sample2',...]
	sampleGroups: list of sample groups in the dataset, ['celltype', 'cell_lineage']
	sampleGroupItems: dict of sample group items keyed on sample group, {'celltype':['B','T',...], 'cell_lineage':['B-Cell Lineage',...]}
	sampleGroupColours: dict of sample group colours keyed on sample group, {'celltype':['#cccccc',...], 'cell_lineage':['#f2f2f2',...]}
	sampleIdsAsGroupItems: dict of sample group items in the same matching order as sampleIds, keyed on sample group,
		{'celltype':['B','B','T','B',...], 'cell_lineage':['B-Cell Lineage','B-Cell Lineage',...]}
'''
import json
%>

<%namespace name="common_elements" file="common.mako"/>

<!doctype html>
<html lang="en">
<head>
	<!-- Load html containing header elements, which are the same for all pages -->
	${common_elements.header_elements()}

	<!-- javascript specific to this page -->
	<script type="text/javascript" src="/js/plotly-latest.min.js"></script>
	
	<script>
	// Define all the variables which come from python. Even though it's possible to inject these variables anywhere
	// using the template variable syntax, mapping them all to one javascript variable here is recommended, 
	// as it makes it easier for long term maintenance.
	var dataFromPython =  {
		datasetNames: ${json.dumps(datasetNames) |n},
		selectedDatasetName: ${json.dumps(selectedDatasetName) |n},
		coords: ${json.dumps(coords) |n},
		sampleIds: ${json.dumps(sampleIds) |n},
		sampleGroups: ${json.dumps(sampleGroups) |n},
		sampleGroupItems: ${json.dumps(sampleGroupItems) |n},
		sampleGroupColours: ${json.dumps(sampleGroupColours) |n},
		sampleIdsAsGroupItems: ${json.dumps(sampleIdsAsGroupItems) |n}
	};
	
	// This is default selected sample group, which can just be the first element of sample groups.
	dataFromPython.selectedSampleGroup = dataFromPython.sampleGroups[0];

	var vm;	// This will be assigned to a Vue instance below. Having this as a global makes it easy to access it from console.
	</script>
</head>

<body>
	<!-- Load html containing menu, which is the same for all pages -->
	${common_elements.banner()}
	
	<div class="content">
		<div class="container">
			<div class="main">
				<h1>PCA</h1>
				<p>This page shows a PCA (principal components analysis) plot of a dataset.</p>
				<div style="margin-top:50px;">
					<p>
						dataset: <select v-model="data.selectedDatasetName" @change="reloadPage"><option v-for="item in data.datasetNames">{{item}}</option></select>
						<select v-model="data.selectedSampleGroup" @change="updatePlot"><option v-for="item in data.sampleGroups">{{item}}</option></select>
					</p>
				</div>
				<div id="mainPlotDiv"></div>
			</div>
			
			<div class="aside">
			<h4>Information about this page</h4>
			<ul>
			<li>views/pca.py contains all methods relevant to this page.</li>
			<li>templates/pca.mako contains the html that renders this page.</li>
			<li>uses <a href="https://plot.ly/" target="_blank">plotly</a> to perform the plot.</li>
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
			data: dataFromPython,
		},
		methods: {	// define all methods used by the Vue instance
			// Function to perform the plot.
			updatePlot: function() {
				var self = this;	// this refers to the Vue instance, and it's safer to map it to another variable
				var traces = [];
				var selectedSampleGroup = self.data.selectedSampleGroup;
				for (var i=0; i<self.data.sampleGroupItems[selectedSampleGroup].length; i++) {
					var groupItem = self.data.sampleGroupItems[selectedSampleGroup][i];
					var sampleIdsInThisGroupItem = self.data.sampleIds.filter(function(item,index) { return self.data.sampleIdsAsGroupItems[selectedSampleGroup][index]==groupItem });
					var trace = {
						x: self.data.coords[0].filter(function(item,index) { return self.data.sampleIdsAsGroupItems[selectedSampleGroup][index]==groupItem }),
						y: self.data.coords[1].filter(function(item,index) { return self.data.sampleIdsAsGroupItems[selectedSampleGroup][index]==groupItem }),
						text: self.data.sampleIdsInThisGroupItem,
						name: groupItem,
						marker: {},
						mode: "markers",
					};
				if (selectedSampleGroup in self.data.sampleGroupColours && groupItem in self.data.sampleGroupColours[selectedSampleGroup])
					trace.marker.color = self.data.sampleGroupColours[selectedSampleGroup][groupItem];
				traces.push(trace);
				}
				Plotly.newPlot("mainPlotDiv", traces, { title: "PCA" });
			},

			// Function to reload this page, specifing a dataset
			reloadPage: function() {
				window.location.href = 'pca?dataset=' + this.data.selectedDatasetName;
			},
		},
		mounted() {	// Vue runs this section after loading the page
			this.updatePlot();
		}
	})
	</script>

</body>
</html>
