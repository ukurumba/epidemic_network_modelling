#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext


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



ext_modules=[
    Extension("enm_cython",
              ["./epidemic_network_modelling/enm_cython.pyx"],
              # libraries=["m"],
              extra_compile_args = ["-O3", "-ffast-math", "-march=native", "/openmp", "-fopenmp" ],
              extra_link_args=['-fopenmp']
              ) 
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
    cmdclass = {'build_ext': build_ext},
    ext_modules=ext_modules,
    test_suite='tests',
    tests_require=test_requirements
)
