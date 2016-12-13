#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from distutils.core import setup
from Cython.Build import cythonize

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='epidemic_network_modelling',
    version='0.1.0',
    description="A program that looks at questions associated with epidemic modelling on networks. ",
    long_description=readme + '\n\n' + history,
    author="Unni Kurumbail",
    author_email='ukurumba@u.rochester.edu',
    url='https://github.com/ukurumba/epidemic_network_modelling',
    packages=[
        'epidemic_network_modelling',
    ],
    package_dir={'epidemic_network_modelling':
                 'epidemic_network_modelling'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='epidemic_network_modelling',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    ext_modules=cythonize('./epidemic_network_modelling/fib.pyx'),
    test_suite='tests',
    tests_require=test_requirements
)
