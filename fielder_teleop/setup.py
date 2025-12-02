from setuptools import find_packages, setup
import sys

package_name = 'fielder_teleop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rsbdev',
    maintainer_email='rapid@robopreneur.com',
    description='ROS2 teleop bridge for Robopreneur Fielder AMR',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
            'setuptools'
        ],
    },
    entry_points={
        'console_scripts': [
            'fielder_teleop = fielder_teleop.fielder_teleop_node:main',
            'fielder_teleop_sub = fielder_teleop.fielder_websocket_node:main'
        ],
    },
    options={
        'build_scripts': {
            'executable': sys.executable,
        },
    }
)
