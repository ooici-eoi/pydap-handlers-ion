#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import os
import sys

# Add /usr/local/include to the path for macs, fixes easy_install for several packages (like gevent and pyyaml)
if sys.platform == 'darwin':
    os.environ['C_INCLUDE_PATH'] = '/usr/local/include'

version = '0.1'

setup(  name = 'pydap.handlers.ion',
        version = version,
        description = 'OOI ION Pydap Handler',
        long_description='''
Pydap is an implementation of the Opendap/DODS protocol, written from
scratch. This handler enables Pydap to serve OOI ION data on the
network for Opendap clients.
        ''',
        url = '',
        download_url = 'http://ooici.net/releases',
        license = 'Apache 2.0',
        author = 'Christopher Mueller',
        author_email = 'cmueller@asascience.com',
        keywords = ['ooici', 'ion', 'pydap', 'eoi'],
        packages = find_packages(),
        test_suite = 'pyon',
        dependency_links = [
            'http://ooici.net/releases'
        ],
        install_requires = [
            'pyon',
            'eoi-services',
            'Pydap==3.0.1',
            'pydap.handlers.netcdf==0.5.0',
            'pydap.responses.netcdf==0.1.3',
            'pydap.responses.wms==0.4.6',
            'pydap.responses.kml==0.4.5',
            'pydap.responses.matlab==0.1.2',
            'arrayterator==1.0.1',
            'netCDF4==0.9.8',
            'cdat_lite==6.0rc2',
            'pyyaml==3.10',
        ],
        entry_points="""
            [pydap.handler]
            ion = pydap.handlers.ion:Handler
        """,
     )
