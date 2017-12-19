<%
'''
This page renders expression profile page.
Required inputs:
	datasetNames: ["lanner",...], a list of dataset names in the system
	selectedDatasetName: "lanner", currently selected dataset
	geneId: "ENSG00000183625", row id of the expression profile to show
	expressionValues: [0.0, 4.18, ...], list of expresson values for the gene
		sampleIds: ${json.dumps(sampleIds) |n},
		sampleGroups: ${json.dumps(sampleGroups) |n},
		sampleGroupItems: ${json.dumps(sampleGroupItems) |n},
		sampleIdsAsGroupItems: ${json.dumps(sampleIdsAsGroupItems) |n}
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
	<script type="text/javascript" src="/js/axios.min.js"></script>

	<script>
	// Define all the variables which come from python. Even though it's possible to inject these variables anywhere
	// using the template variable syntax, mapping them all to one javascript variable here is recommended, 
	// as it makes it easier for long term maintenance.
	var dataFromPython =  {
		datasetNames: ${json.dumps(datasetNames) |n},
		selectedDatasetName: ${json.dumps(selectedDatasetName) |n},
		geneId: ${json.dumps(geneId) |n},
		expressionValues: ${json.dumps(expressionValues) |n},
		sampleIds: ${json.dumps(sampleIds) |n},
		sampleGroups: ${json.dumps(sampleGroups) |n},
		sampleGroupItems: ${json.dumps(sampleGroupItems) |n},
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
				<h1>Expression</h1>
				<p>This page shows the expression profile plot of a selected gene from the Genes page.</p>
				<div>
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
			<li>views/expression.py contains all methods relevant to this page.</li>
			<li>templates/expression.mako contains the html that renders this page.</li>
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
				// Each sample group item is a trace (eg. ['B','T'] if celltype was the sample group)
				for (var i=0; i<self.data.sampleGroupItems[selectedSampleGroup].length; i++) {
					var groupItem = self.data.sampleGroupItems[selectedSampleGroup][i];
					var sampleIdsInThisGroupItem = self.data.sampleIds.filter(function(item,index) { return self.data.sampleIdsAsGroupItems[selectedSampleGroup][index]==groupItem });
					var trace = {
						y: self.data.expressionValues.filter(function(item,index) { return self.data.sampleIdsAsGroupItems[selectedSampleGroup][index]==groupItem }),
						//y:[1,2,3],
						name: groupItem,
						boxpoints: 'all',
						type: "box",
					};
					console.log(groupItem, JSON.stringify(trace));
					traces.push(trace);
				}
				Plotly.newPlot("mainPlotDiv", traces, { title: self.data.geneId });
			},

			// Function to reload this page, specifing a dataset
			reloadPage: function() {
				window.location.href = 'expression?dataset=' + this.data.selectedDatasetName;
			},
		},

		mounted() {	// Vue runs this section after loading the page
			this.updatePlot();
		}
	})
	</script>

</body>
</html>
