from setuptools import setup

package_name = 'assembly_pipeline'

setup(
    name=package_name,
    version='1.0.0',
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

    description='Manufacturing Assembly Planning Pipeline in ROS2',
    license='Apache License 2.0',

    entry_points={
        'console_scripts': [
            'cad_loader = assembly_pipeline.cad_loader:main',
            'feature_analyser = assembly_pipeline.feature_analyser:main'
            'operation_reasoner = assembly_pipeline.operation_reasoner:main'
            'instruction_generator = assembly_pipeline.instruction_generator:main'
        ],
    },
)