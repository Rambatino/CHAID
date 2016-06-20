"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/Rambatino/CHAID
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CHAID',
    version='0.0.7',
    description='A CHAID tree building algorithm',
    long_description=long_description,
    url='https://github.com/Rambatino/CHAID',
    author='Mark Ramotowski, Richard Fitzgerald',
    author_email='mark.tint.ramotowski@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='CHAID pandas numpy scipy statistics statistical analysis',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['numpy', 'scipy', 'pandas', 'treelib'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    }
)