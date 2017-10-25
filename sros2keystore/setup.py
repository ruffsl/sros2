from setuptools import find_packages
from setuptools import setup

setup(
    name='sros2keystore',
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    install_requires=['setuptools'],
    author='Ruffin White',
    author_email='ruffin@osrfoundation.org',
    maintainer='Ruffin White',
    maintainer_email='ruffin@osrfoundation.org',
    url='https://github.com/ros2/sros2',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='SROS2 provides tools to help manage security keys.',
    long_description="""\
SROS2 provides command-line tools to help generate and distribute keys and \
certificates which are then used by supported middleware implementations to \
enhance the security of ROS 2 deployments.""",
    license='Apache License, Version 2.0',
    test_suite='test',
    entry_points={
        'ros2cli.command': [
            'keystore = sros2keystore.command.keystore:KeystoreCommand',
        ],
        'ros2cli.extension_point': [
            'sros2keystore.verb = sros2keystore.verb:VerbExtension',
        ],
        'sros2keystore.verb': [
            'auto = sros2keystore.verb.auto:AutoVerb',
            'build = sros2keystore.verb.build:BuildVerb',
            'create = sros2keystore.verb.create:CreateVerb',
            'init = sros2keystore.verb.init:InitVerb',
            'sign = sros2keystore.verb.sign:SignVerb',
        ],
    }
)
