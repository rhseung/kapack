from setuptools import setup

setup(
    name='kap',
    version='1.0',
    py_modules=['kap'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        kap=kap:cli
    ''',
)
