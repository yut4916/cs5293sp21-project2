from setuptools import setup, find_packages

setup(
	name='project2',
	version='1.0',
	author='Katherine (Katy) Yut',
	author_email='katherine.yut@ou.edu',
	packages=find_packages(exclude=('docs')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)
