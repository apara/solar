try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Read the data from the solar array into the database',
    'author': 'Alex Paransky',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'My email.',
    'version': '0.1',
    'install_requires': [],
    'packages': ['reader'],
    'scripts': [],
    'name': 'solar'
}

setup(**config)
