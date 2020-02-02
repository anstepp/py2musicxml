from setuptools import setup, find_namespace_packages

setup(
	name='py2musicxml',
	description='python library for prototyping compositional ideas',
	author='Aaron Stepp, Rachel House',
	author_email='stepp.aaron@gmail.com',
	version='0.1',
	packages=find_namespace_packages(),
	tests_require=['pytest'],
)
