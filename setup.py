# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as fr:
    required = fr.read().splitlines()

setup(
    name='scadlira',
    version='0.0.1',
    packages=['scadlira'],
    url='https://github.com/ndrwpvlv/scadlira',
    license='',
    author='Andrei S. Pavlov',
    author_email='ndrw.pvlv@gmail.com',
    description='SCAD to Lira-SAPR input file converter',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
)