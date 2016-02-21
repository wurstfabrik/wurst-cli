# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from wurstc import __version__

ENTRY_POINTS = """
[console_scripts]
wurst = wurstc.cli:main
"""

requirements = open("requirements.txt").readlines()
dev_requirements = open("requirements-dev.txt").readlines()

setup(
    name='wurstc',
    version=__version__,
    license='MIT',
    packages=find_packages('.'),
    include_package_data=True,
    tests_require=dev_requirements,
    install_requires=requirements,
    zip_safe=True,
    entry_points=ENTRY_POINTS
)
