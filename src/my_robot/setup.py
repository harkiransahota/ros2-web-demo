from setuptools import setup

package_name = 'my_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],

    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],

    install_requires=['setuptools'],
    zip_safe=True,

    maintainer='Harkiran Sahota',
    maintainer_email='harkiran.sahota@gmx.de',

    description='ROS2 velocity publisher',
    license='Apache License 2.0',

    entry_points={
        'console_scripts': [
            'velocity_publisher = my_robot.velocity_publisher:main',
        ],
    },
)