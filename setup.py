import glob
from setuptools import setup, find_packages

setup(
	name='ptty',
	version='0.1',
	author='https://github.com/Pebaz',
	py_modules=['ptty'],
	entry_points={
		'console_scripts' : [
			'ptty=ptty:term'
		]
	}
)
