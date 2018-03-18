from distutils.command.install_data import install_data

from setuptools import setup, find_packages

VERSION = "0.1.0"
with open("LICENSE") as f:
    LICENSE = f.read()
with open("README.md") as f:
    README = f.read()

setup(
        name='docker_hosts_update',
        version=VERSION,
        author='Joakim Uddholm',
        author_email='tethik@gmail.com',
        description='Service that automatically updates your /etc/hosts file based on your running docker containers.',
        long_description=README,
        url='https://github.com/Tethik/docker_hosts_update',
        py_modules=['docker_hosts_update'],
        entry_points = {
            'console_scripts': ['docker-hosts-update=docker_hosts_update:main'],
        },
        package_data={'': ['LICENSE', 'README.md']},
        include_package_data=True,
        install_requires=[
            'docker',
            'click',
            'click-log'
        ],
        tests_require=[
            'pytest',
            'pytest-cov',
            'pylint',
        ],
        license=LICENSE,
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python',
            'Topic :: Internet',
        ])
