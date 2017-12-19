<%
'''
There's no required inputs for this template.
Note that to access a python injected variable here, use context.get() function.
'''
import json
%>

<!DOCTYPE html>
<html lang="en">
<head>
	<%namespace name="common_elements" file="common.mako"/>
	${common_elements.header_elements()}
</head>
<body>
	${common_elements.banner()}
	<div class="content">
		<div class="container">
			<div class="main">
				<h1>Welcome to BioPyramid</h1>
				<p>BioPyramid is a python package that can be used as a template or a scaffold, upon which you can build your own
				genomics data portal. An example of such a data portal using BioPyramid code is 
				<a href="http://haemosphere.org">haemosphere.org</a>.</p>
			
				<p>Even though it is built on python's pyramid framework, knowledge of pyramid is not required to get started, 
				as most of the basic components have been transparently included in the code. Basic requirement is some 
				experience in python.
				</p>
				
				<p>Get started by exploring the basic functionality using the example dataset provided.
				Then start modifying the code or adding new datasets to customise the application.
				</p>

				<p>More detailed instructions are at the <a href="http://github.com/jarny/biopyramid">github page</a>.
				</p>
			</div>
			
			<div class="aside">
			<h3>Citing BioPyramid</h3>
			<p>Coming soon. Please refer to the <a href="http://github.com/jarny/biopyramid">github page</a> for now.</p>
			</div>
		</div>
	</div>
	${common_elements.footer()}
</body>
</html>
