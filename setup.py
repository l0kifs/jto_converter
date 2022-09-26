from setuptools import setup, find_packages

setup(
    name='jto',
    version='1.0.0',
    author='l0kifs',
    license='Apache 2.0',
    packages=find_packages(),
    package_data={'': ['*.json']},
    include_package_data=True
)