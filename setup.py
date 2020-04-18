"""`setup.py`"""
from setuptools import setup, find_packages

# # Package requirements
# with open('requirements.txt') as f:
#     INSTALL_REQUIRES = [l.strip() for l in f.readlines() if l]

INSTALL_REQUIRES=[
'numpy',
'scikit-learn',
'pandas',
'surprise',
'scipy',
'scikit-surprise',
'networkx',
]

setup(name='hinpy',
      version='0.1.7',
      description='A python framework for Heterogeneous Information Networks.',
      author='Pedro Ramaciotti Morales',
      author_email='pedro.ramaciotti@gmail.com',
      url = 'https://github.com/pedroramaciotti/HINPy',
      download_url = 'https://github.com/pedroramaciotti/HINPy/archive/0.1.7.tar.gz',
      keywords = ['Heterogeneous Information Networks','Recommender Systems','Diversity','Echo Chamber','Filter Bubble'],
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES)
