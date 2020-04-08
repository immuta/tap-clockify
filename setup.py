#!/usr/bin/env python
import setuptools

setuptools.setup(
    name="tap-clockify",
    version="0.1.0",
    description="Singer.io tap for extracting data",
    author="Stephen Bailey",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_clockify"],
    entry_points="""
        [console_scripts]
        tap-clockify=tap_clockify:main
    """,
    packages=setuptools.find_packages(),
    package_data = {
        "schemas": ["tap_clockify/schemas/*.json"]
    },
    include_package_data=True,
)
