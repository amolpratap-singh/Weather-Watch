from setuptools import setup, find_packages

setup(
    name='weatherapp',
    version='0.0.1',
    description='Weather Main App',
    long_description='Weather main app is build for to retrieve weather and aqi information',
    packages=find_packages(),
    author='Amolpratap Singh',
    author_email='amolpratap.singh@yahoo.com',
    install_requires=[
        # List your package dependencies here
        'opensearch-py',
        'python-dateutil',
        'pytz',
        'requests',
        'schedule',
        'urllib3'
    ],
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
