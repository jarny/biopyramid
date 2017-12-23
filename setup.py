import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'Readme.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pandas',
    'tables',
    'pastedeploy',
    'pyramid',
    'pyramid_mako',
    'pyramid_beaker',
    'pyramid_debugtoolbar',
    'genedataset>=1.0.0a',
    'waitress',
    ]

setup(name='biopyramid',
      version='0.1',
      description='biopyramid',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Jarny Choi',
      author_email='jarnyc@unimelb.edu.au',
      url='http://github.com/jarny/biopyramid',
      keywords='web pyramid bioinformatics',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="biopyramid",
      entry_points="""\
      [paste.app_factory]
      main = biopyramid:main
      """,
      )
