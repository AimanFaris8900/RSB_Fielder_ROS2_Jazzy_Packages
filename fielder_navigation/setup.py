from setuptools import find_packages, setup
from glob import glob
import sys
import os

package_name = 'fielder_navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Add launch files
        (os.path.join('share', package_name, 'launch'), 
            glob('launch/*.py')),
        # add config files - try with explicit path
        (os.path.join('share', package_name, 'config'), 
            glob(os.path.join('config', '*.yaml'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rsbdev',
    maintainer_email='aimanfaris.af@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
            'setuptools'
        ],
    },
    entry_points={
        'console_scripts': [
            'fielder_odom = fielder_navigation.fielder_odometry_node:main',
            'fielder_pc2 = fielder_navigation.fielder_scan_node:main',
        ],
    },
    options={
        'build_scripts': {
            'executable': sys.executable,
        },
    },
)