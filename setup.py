from setuptools import setup, find_packages

setup(name='reposync',
        version='1.0a',
        author='Tom Howe',
        author_email='turtlebender@gmail.com',
        packages=['.'],
        install_requires=[ 'pyinotify' ],
        scripts=[ 'scripts/repopush', 'scripts/repopull' ]
        )
