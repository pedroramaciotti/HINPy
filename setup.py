"""`setup.py`"""
from setuptools import setup, find_packages

# # Package requirements
# with open('requirements.txt') as f:
#     INSTALL_REQUIRES = [l.strip() for l in f.readlines() if l]

INSTALL_REQUIRES=[
'matplotlib',
'networkx',
'numpy',
'pandas',
'scikit-learn',
'scikit-surprise',
'scipy',
]

setup(name='hinpy',
      version='0.1.11',
      description='A python framework for Heterogeneous Information Networks.',
      author='Pedro Ramaciotti Morales',
      author_email='pedro.ramaciotti@gmail.com',
      url = 'https://github.com/pedroramaciotti/HINPy',
      download_url = 'https://github.com/pedroramaciotti/HINPy/archive/0.1.11.tar.gz',
      keywords = ['Heterogeneous Information Networks','Recommender Systems','Diversity','Echo Chamber','Filter Bubble'],
      packages=find_packages(),
      #license='apache-2.0',
      #classifiers=["License :: OSI Approved :: Apache License, Version 2.0 (Apache-2.0)"],
      data_files=[('', ['LICENSE'])],
      install_requires=INSTALL_REQUIRES)
