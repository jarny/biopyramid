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
2. Install BioPyramid by running (from within the repository directory):
```bash
python setup.py develop
```
3. Start the pyramid server:
```bash
pserve development.ini
```

If you're using conda and would like to install BioPyramid in a separate environment, insert these steps between 1 and 2:
- Install conda
- Create the required environment by running:
```bash
conda env create -f environment.yml
```

If successful, you will be able to go to the URL shown by the pserve command on your browser.

Note that this repo contains a 33Mb example dataset.

## How to use it
BioPyramid comes with an example dataset, so you should be able to play with it to test out its main features. Then the next step may be to create your own dataset file and upload it - read the section on dataset creation below for more details on how to do this.

After that, you can modify the code to customise it to your own application. For those not familiar with the code structure of python pyramid, here is a schematic of the components which make up biopyramid and some description of each part to get started.

![Schematic](/biopyramid/static/images/Schematic.png)

- biopyramid/models/ contains data models which should exist independently of the pyramid application. This is also a suitable place to create extensions of the existing classes such as genedataset, and an example is provided by bpdataset.py, which has BPDataset class that inherits from genedataset.Dataset class. 
- biopyramid/static/ contains static resources, including images, styles sheets, javascript packages and static html.
- biopyramid/templates/ contains Mako templates used to render pages or parts of pages. Each page is injected with variables from the python controller and these can be used to dynamically render the page appropriately.
- biopyramid/views/ contains controllers whose functions are read by pyramid at start-up. The functions with @view_config decorators should map to URLs as specified in biopyramid/__init__.py. The grouping of the functions into individual scripts is for convenience.

## How to add a dataset
To add a dataset to BioPyramid, first create the HDF file required for instantiating the bpdataset.BPDataset class. Then simply place this file inside data/datasets/ directory. The application will look for all files in this directory with suffix "h5" and read them as available datasets.

Here is a step by step description of how the example dataset file included with BioPyramid, "haemopedia.2.7.h5", was created, so that it can be used as a template for additional dataset creation.
```python
import pandas
from biopyramid.models import bpdataset


# Read sample table
samples = pandas.read_csv("samples.txt", sep="\t", index_col=0)

# We can define which columns of the sample table should be "selectable" within BioPyramid.
# Selectable columns can be used to group samples in a plot, for example, while the other columns are ignored.
sampleGroupsDisplayed = ["celltype", "cell_lineage", "tissue"]

# For each sample group (=column of sample table), we can choose how the items should be ordered
sampleGroupOrdering = {'cell_lineage': ['Multi Potential Progenitor', 'Restricted Potential Progenitor', 
                                        'Erythrocyte Lineage', 'Megakaryocyte Lineage', 'Mast Cell Lineage', 
                                        'Basophil Lineage', 'Eosinophil Lineage', 'Neutrophil Lineage', 
                                        'Macrophage Lineage', 'Dendritic Cell Lineage', 'B Cell Lineage', 
                                        'T Cell Lineage', 'NK Cell Lineage'], 
                       'celltype': ['LTHSC', 'STHSC', 'MPP', 'CMP', 'PreGM1', 'PreGM2', 'GMP', 'FcgRBP', 
                                    'CD9Hi', 'BEMP', 'CLP', 'PreCFUE', 'MEP', 'CFUE', 'EryBlPB', 'EryBlPO', 
                                    'Retic', 'Meg8N', 'Meg16N', 'Meg32N', 'Mast', 'Baso', 'EoP', 'Eo', 'NeutLN', 
                                    'NeutPt', 'MonoPB', 'MonoLN', 'Mac', 'CDP', 'cDC1', 'cDC2', 'MigDC', 'ProB', 
                                    'PreB', 'ImmB', 'B1', 'B2', 'MatB', 'CD4TThy1lo', 'TN1', 'TN2', 'TN3', 'TN4', 
                                    'DblPosT', 'NveCD4T', 'NveCD8T', 'EffCD4T', 'EffCD8T', 'CD4TLN', 'CD8TLN', 
                                    'RegT', 'MemCD8T', 'NK']
                      }

# Also we can choose colours for each sample group item if we choose to
sampleGroupColours = {'cell_lineage': 
                          {'Multi Potential Progenitor': 'rgb(190,190,190)', 
                           'Erythrocyte Lineage': 'rgb(139,0,0)', 
                           'NK Cell Lineage': 'rgb(34,139,34)', 
                           'Mast Cell Lineage': 'rgb(255,20,147)', 
                           'Eosinophil Lineage': 'rgb(255,140,105)', 
                           'Macrophage Lineage': 'rgb(171,130,255)', 
                           'Dendritic Cell Lineage': 'rgb(30,144,255)', 
                           'Basophil Lineage': 'rgb(205,55,0)', 
                           'T Cell Lineage': 'rgb(0,255,0)', 
                           'Neutrophil Lineage': 'rgb(104,34,139)', 
                           'Megakaryocyte Lineage': 'rgb(238,180,34)', 
                           'B Cell Lineage': 'rgb(0,0,255)', 
                           'Restricted Potential Progenitor': 'rgb(127,127,127)'}
                     }


# Read expression matrix - quantile normalised, mapped to gene ids, then aggregated for multiple probes
expression = pandas.read_csv("normalised_expression.txt", sep="\t", index_col=0)

# Check that all columns of expression matrix are found in the sample table
assert set(expression.columns).issubset(set(samples.index))

# Create coordinates of PCA, used to plot this quickly
from sklearn.decomposition import PCA
import numpy
fit = PCA(n_components=2).fit_transform(expression.transpose()) # PCA function works on rows so transpose
pca = pandas.DataFrame(fit, index=expression.columns, columns=['x','y'])

# Dataset metadata
attributes = {'name': 'haemopedia',
              'fullname': 'Haemopedia',
              'description': 'Microarray gene expression profiles from a comprehensive range of wildtype murine blood cells, all generated by Hilton Lab (Walter and Eliza Hall Institute) over a number of years.', 
              'expression_data_keys': ['normalised'],
              'pubmed_id': '27499199', 
              'species': 'MusMusculus', 
              'version': '2.7'}

# Finally ready to create the file
bpdataset.createDatasetFile(".", 
                            attributes=attributes,
                            samples=samples,
                            expressions=[expression],
                            sampleGroupsDisplayed=sampleGroupsDisplayed,
                            sampleGroupOrdering=sampleGroupOrdering,
                            sampleGroupColours=sampleGroupColours,
                            pca=pca,
                            )
# This would create "haemopedia.2.7.h5" file in the current directory.
```



