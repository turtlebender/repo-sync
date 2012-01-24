from distutils.core import setup

setup(name='reposync',
        version='1.0a',
        author='Tom Howe',
        author_email='turtlebender@gmail.com',
        packages='reposync'
        install_requires=[ 'pyinotify' ],
        scripts=[ 'reposync/reposync', 'reposync/repomonitor' ]
        )
