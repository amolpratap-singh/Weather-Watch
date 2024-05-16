from setuptools import setup, find_packages

setup(
    name='weatherapp',
    version='1.0.0',
    packages=find_packages(),
    #install_requires=[
        # List your package dependencies here
    #    'requests',
        # Add any other dependencies required by your package
    #],
    #tests_require=[
    #    # List your test dependencies here
    #    'pytest',
        # Add any other dependencies required for testing
    #],
    entry_points={
        'console_scripts': [
            'weatherapp=weatherapp.main:main',
        ],
    },
)
