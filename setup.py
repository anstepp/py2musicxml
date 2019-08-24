from setuptools import setup

setup(
	name='py2musicxml',
	description='python library for prototyping compositional ideas',
	author='Aaron Stepp, Rachel House',
	author_email='anstepp@indiana.edu',
	version='0.1',
	packages=['py2musicxml'],
	entry_points={
		'console_scripts': ['py2musicxml = py2musicxml.__main__:main']
	},
	tests_require=['pytest'],
)
