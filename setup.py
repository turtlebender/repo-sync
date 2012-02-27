from setuptools import setup, find_packages

setup(name='reposync',
        zip_safe=False,
        version='1.0a',
        author='Tom Howe',
        author_email='turtlebender@gmail.com',
        packages=['reposync'],
        install_requires=[ 'pyinotify' ],
        scripts=[ 'scripts/repopush', 'scripts/repopull', 'scripts/reposync' ]
        )
