<%
"""This template contains html elements which are common to all or many pages.
Create a block of html inside a <%def></%def> enclosure and call it from any page.
See any of the included pages such as gene.mako for an example of how it is called."""
%>

<%def name="header_elements()">

<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>BioPyramid</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="Description" lang="en" content="Gene Expression Analysis Tool">
<meta name="author" content="Jarny Choi">
<meta name="keywords" content="python web application biopyramid" />
<meta name="robots" content="index, follow">

<!-- icons -->
<link rel="shortcut icon" href="favicon.ico">


<!-- styles -->
<link rel="stylesheet" href="/css/default_stylesheet.css">
<style>
div.container {
	max-width: 80em;
}
div.main {
	width: 70%;
}
div.aside {
	margin-top:40px;
	width: 25%;
}
</style>

<!-- javascript -->
<script type="text/javascript" src="/js/vue.min.js"></script>

</%def>

<!--------------------------------------------------------------------------------------->
<%def name="banner()">
<div class="header">
	<div class="container">
		<h1 class="header-heading">
			<a href="/" style="text-decoration:none; color:#ffffff;">BioPyramid</a>
		</h1>
	</div>
</div>
<div class="nav-bar">
	<div class="container">
		<ul class="nav">
			<li><a href="/">About</a></li>
			<li><a href="/datasets">Datasets</a></li>
			<li><a href="/genes">Genes</a></li>
			<li><a href="/pca">PCA</a></li>
			<li><a href="/expression">Expression</a></li>
		</ul>
	</div>
</div>
</%def>

<!--------------------------------------------------------------------------------------->
<%def name="footer()">
<style>
	.footer a {
		text-decoration:none;
		color: #ffffff;
	}
</style>
<div class="footer">
	<div class="container">
		<a href="http://github.com/jarny/biopyramid">BioPyramid version 0.1</a>
	</div>
</div>
</%def>
