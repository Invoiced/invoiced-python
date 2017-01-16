import os
import sys
import warnings

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

install_requires = []

if sys.version_info < (3, 0):
    warnings.warn(
        'Python 2 is not supported.',
        DeprecationWarning)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'invoiced'))
from version import VERSION

with open('LONG_DESCRIPTION.rst') as f:
    long_description = f.read()

setup(
    name='invoiced',
    version=VERSION,
    description='Invoiced client library',
    long_description=long_description,
    author='Invoiced',
    author_email='support@invoiced.com',
    url='https://github.com/invoiced/invoiced-python',
    packages=['invoiced', 'invoiced.test'],
    install_requires=[
        'requests >= 2.0.0',
        'inflection == 0.3.1'
    ],
    extras_require={
        'requests': ['security>=2.0.0']
    },
    test_suite='invoiced.test.all',
    tests_require=['responses == 0.5.0'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ])
