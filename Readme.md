BioPyramid
======
**BioPyramid** is a python and javascript based framework for developing an online genomics application. It can be used as a starting scaffold or a template. BioPyramid contains a number of components designed to reduce the time and effort in building such an application from scratch, including gene annotation, dataset models and visualisation tools.

## Key Components
BioPyramid contains the following set of ready-made modules:
- Dataset models which can be used to store and query a dataset, such as expression values of a selected gene in selected samples. 
- Geneset models which contain data about commonly used gene annotations, such as Ensembl and Entrez IDs, synonyms and orthologues. 
- Javascript based visualisation tools, including principle components plot and expression profile plot.

BioPyramid uses minimal set of very transparent code with clear documentation that you can start modifying without being an expert in python pyramid framework. It comes with an example dataset so you can see how it works.

## How to install it
1. Clone this repo.
2. Install conda
3. Create the required environment by running:
```bash
conda env create -f environment.yml
```
4. Install BioPyramid by running (from within the repository directory):
```bash
python setup.py develop
```
5. Start the pyramid server:
```bash
pserve development.ini
```

If successful, you will be able to go to the URL shown by the pserve command on your browser.

Note that this repo contains a large (650+Mb) example dataset.

## How to use it
BioPyramid comes with an example dataset, so you should be able to play with it to test out its main features. Then the next step may be to create your own dataset file and upload it - read the section on dataset creation below for more details on how to do this.

After that, you can modify the code to customise it to your own application. For those not familiar with the code structure of python pyramid, here is a schematic of the components which make up biopyramid and some description of each part to get started.
![Schematic](/biopyramid/static/images/Schematic.png)

- biopyramid/models/ contains data models which should exist independently of the pyramid application. This is also a suitable place to create extensions of the existing classes such as genedataset, and an example is provided by bpdataset.py, which has BPDataset class that inherits from genedataset.Dataset class. 
- biopyramid/static/ contains static resources, including images, styles sheets, javascript packages and static html.
- biopyramid/templates/ contains Mako templates used to render pages or parts of pages. Each page is injected with variables from the python controller and these can be used to dynamically render the page appropriately.
- biopyramid/views/ contains controllers whose functions are read by pyramid at start-up. The functions with @view_config decorators should map to URLs as specified in biopyramid/__init__.py. The grouping of the functions into individual scripts is for convenience.

## How to add a dataset
To add a dataset to BioPyramid, first create the HDF file required for instantiating the bpdataset.BPDataset class. See below for more detail including an example. Then simply place this file inside data/datasets/ directory. The application will look for all files in this directory with suffix "h5" and read them as available datasets.

Here is a step by step description of how the example dataset file included with BioPyramid, "lanner.1.0.h5", was created, so that it can be used as a template for additional dataset creation.
```python
import pandas
from biopyramid.models import bpdataset

# Read sample table
samples = pandas.read_csv("phenotype_information.txt", sep="\t", index_col=0)

# We can define which columns of the sample table should be "selectable" within BioPyramid.
# Selectable columns can be used to group samples in a plot, for example, while the other columns are ignored.
sampleGroupsDisplayed = ["Cell_pheno", "Donor"]

# For each sample group (=column of sample table), we can choose how the items should be ordered
sampleGroupOrdering = {'Cell_pheno':['E3', 'E4', 'E4-Late', 'E5-Early', 'E5', 'E6', 'E7'],
                       'Donor':sorted(set(samples['Donor']))}

# Also we can choose colours for each sample group item if we choose to
sampleGroupColours = {'Cell_pheno':
                            {'E3':"#cbc9e2", 
                             'E4':"#bae4b3", 
                             'E4-Late':"#74c476", 
                             'E5-Early':"#fcddab", 
                             'E5':"#ef9708", 
                             'E6':"#9cded6", 
                             'E7':"#f0aaab"}
                      }

# Read expression matrix - these are cpm values (not logged)
cpm = pandas.read_csv("cpm.1.0.txt", sep="\t", index_col=0)

# Check that all columns of expression matrix are found in the sample table
assert set(cpm.columns).issubset(set(samples.index))

# Create coordinates of PCA, used to plot this quickly
from sklearn.decomposition import PCA
import numpy
fit = PCA(n_components=2).fit_transform(numpy.log2(cpm+1).transpose()) # PCA function works on rows so transpose
pca = pandas.DataFrame(fit, index=cpm.columns, columns=['x','y'])

# Dataset metadata
attributes = {'name': 'lanner', 
              'fullname': 'Lanner',
              'description': 'Single-Cell RNA-Seq Reveals Lineage and X Chromosome Dynamics in Human Preimplantation Embryos',
              'expression_data_keys': ['cpm'],
              'pubmed_id': '27062923', 
              'species': 'HomoSapiens', 
              'version': '1.0'}

# Finally ready to create the file
bpdataset.createDatasetFile(".", 
                            attributes=attributes,
                            samples=samples,
                            expressions=[cpm],
                            sampleGroupsDisplayed=sampleGroupsDisplayed,
                            sampleGroupOrdering=sampleGroupOrdering,
                            sampleGroupColours=sampleGroupColours,
                            pca=pca,
                            )
# This would create "lanner.1.0.h5" file in the current directory.
```



