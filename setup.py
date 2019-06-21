"""`setup.py` file of stream_graph"""
from setuptools import setup, find_packages

# Package requirements
with open('requirements.txt') as f:
    INSTALL_REQUIRES = [l.strip() for l in f.readlines() if l]

setup(name='hinpy',
      version='0.1',
      description='A framework for the analysis of diversity of recommendations in Heterogeneous Information Networks.',
      author='Pedro Ramaciotti Morales [LIP6]',
      author_email='Yiannis.Siglidis@lip6.fr',
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES)
