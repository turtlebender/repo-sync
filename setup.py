from setuptools import setup, find_packages

setup(name='reposync',
        version='1.0a1',
        author='Tom Howe',
        author_email='turtlebender@gmail.com',
        packages=['reposync'],
        install_requires=[ 'pyinotify' ],
        scripts=[ 'scripts/repopush', 'scripts/repopull', 'scripts/reposync' ]
        )
