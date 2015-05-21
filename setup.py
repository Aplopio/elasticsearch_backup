#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [line.strip() for line in open('requirements.txt').readlines()]

setup(
    name='elasticsearch_backup',
    version='0.1.0',
    description="Backup elastic search by taking snapshots.",
    long_description=readme + '\n\n' + history,
    author="Vedarth Kulkarni",
    author_email='vedarth@aplopio.com',
    url='https://github.com/Aplopio/elasticsearch_backup',
    packages=[
        'elasticsearch_backup',
    ],
    package_dir={'elasticsearch_backup':
                 'elasticsearch_backup'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='elasticsearch_backup',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=['pytest']
)
