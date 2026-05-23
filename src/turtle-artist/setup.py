from setuptools import find_packages, setup

package_name = 'turtle-artist'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name,
        ['turtle_artist/input.jpeg']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='guco',
    maintainer_email='gucolombini@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'draw_image = turtle_artist.draw_image:main'
        ],
    },
)
