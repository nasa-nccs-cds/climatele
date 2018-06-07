#!/usr/bin/env python

from distutils.core import setup

setup(name='climatele',
      version='1.0',
      description='Exploratory project for computing the normal modes of the climate system and investigating teleconnections and predictability',
      author='Thomas Maxwell',
      author_email='thomas.maxwell@nasa.gov',
      url='https://github.com/nasa-nccs-cds/climatele.git',
      packages=['climatele', 'climatele.EOFs', 'climatele.test'],
)
