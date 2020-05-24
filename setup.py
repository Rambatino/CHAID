"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/Rambatino/CHAID
"""

import re
from os import path
from setuptools import setup, find_packages


def get_version():
    """
    Read version from __init__.py
    """
    version_regex = re.compile(
        '__version__\\s*=\\s*(?P<q>[\'"])(?P<version>\\d+(\\.\\d+)*(-(alpha|beta|rc)(\\.\\d+)?)?)(?P=q)'
    )
    here = path.abspath(path.dirname(__file__))
    init_location = path.join(here, "CHAID/__init__.py")

    with open(init_location) as init_file:
        for line in init_file:
            match = version_regex.search(line)

    if not match:
        raise Exception(
            "Couldn't read version information from '{0}'".format(init_location)
        )

    return match.group('version')

setup(
    name='CHAID',
    version=get_version(),
    description='A CHAID tree building algorithm',
    long_description="This package provides a python implementation of the Chi-Squared Automatic Inference Detection (CHAID) decision tree",
    url='https://github.com/Rambatino/CHAID',
    author='Mark Ramotowski, Richard Fitzgerald',
    author_email='mark.tint.ramotowski@gmail.com',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='CHAID pandas numpy scipy statistics statistical analysis',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'cython',
        'numpy',
        'pandas',
        'treelib',
        'pytest',
        'scipy',
        'savReaderWriter',
        'graphviz',
        'plotly',
        'colorlover',
        'enum34; python_version == "2.7"'
    ],
    extras_require={
        'test': ['codecov', 'tox', 'tox-pyenv', 'detox', 'pytest', 'pytest-cov', 'psutil'],
    }
)
