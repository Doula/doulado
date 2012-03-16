#import os
#import sys
from setuptools import find_packages
from setuptools import setup

version = '0.0'
requires = []

setup(name='doula-op-tools',
      version=version,
      description="",
      long_description=open('README.rst'),
      classifiers=[], 
      keywords='',
      author='doula committers',
      author_email='',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""
      """,
      )
