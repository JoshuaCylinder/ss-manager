from setuptools import setup


with open("README.md", "r") as f:
    setup(
        name='ss-manager',
        version='1.0.0',
        description='This project is a tool for sharing Shadowsocks protocol dedicated line nodes, '
                    'written in Python and relying on the ss-manager executable program of shadowsocks-libev.',
        long_description=f.read(),
        packages=['ss_manager', 'ss_manager.utils'],
        install_requires=[
            "prettytable",
            "pycryptodome",
        ],
        entry_points={
            'console_scripts': [
                'ss-managerd = ss_manager.main:main',
            ],
        }
    )
