#!/usr/bin/env python3

from setuptools import setup, find_packages

import can_filter_calc

setup(
    name='CAN filter calculator',
    version=can_filter_calc.__version__,
    description='Calculate filters for CAN message IDs.',
    author='optantarus',
    license='MIT',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            'can_filter_calc = can_filter_calc.can_filter_calc:main',
        ]
    },
    install_requires=[
        "more_itertools>=8.4.0"
    ],
    zip_safe=False
) 
