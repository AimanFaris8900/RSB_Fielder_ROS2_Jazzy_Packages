from setuptools import find_packages, setup

package_name = 'fielder_odometry'

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
    description='TODO: ROS2 odometry bridge for Robopreneur Fielder AMR',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
            'setuptools'
        ],
    },
    entry_points={
        'console_scripts': [
            'talker = fielder_odometry.fielder_odometry_node:main',
            'fielder_teleop = fielder_odometry.fielder_teleop_node:main'
        ],
    },
)
