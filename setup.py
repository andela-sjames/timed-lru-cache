"""
A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='timed_lru_cache',
    version='0.1.0',
    description='A time constraint LRUCache Implementation',
    long_description=long_description,
    url='https://github.com/andela-sjames/timed-lru-cache',

    # Author details
    author='Samuel James',
    author_email='samuelvarejames@gmail.com',

    license='MIT',

    keywords='timed lru cache implementation',

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[],
)
