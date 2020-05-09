#!/usr/bin/env python
import setuptools

setuptools.setup(
    name="tap-clockify",
    version="0.2.0",
    description="Singer.io tap for extracting data",
    author="Stephen Bailey",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    packages=setuptools.find_packages(),
    py_modules=["tap_clockify"],
    package_data={"schemas": ["tap_clockify/schemas/*.json"]},
    entry_points="""
        [console_scripts]
        tap-clockify=tap_clockify:main
    """,
    install_requires=["singer-python", "requests"],
    include_package_data=True,
)
