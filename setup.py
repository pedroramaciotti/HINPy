"""`setup.py`"""
from setuptools import setup, find_packages

# Package requirements
with open('requirements.txt') as f:
    INSTALL_REQUIRES = [l.strip() for l in f.readlines() if l]

setup(name='hinpy',
      version='0.1',
      description='A framework for the analysis of diversity in Heterogeneous Information Networks.',
      author='Pedro Ramaciotti Morales',
      author_email='pedro.ramaciotti@gmail.com',
      url = 'https://github.com/pedroramaciotti/HINPy',
      keywords = ['Heterogeneous Information Networks','Recommender Systems','Diversity']
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES)
