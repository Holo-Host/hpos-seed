from setuptools import setup

setup(
    name='hpos-seed',
    packages=['hpos_seed'],
    entry_points={
        'console_scripts': [
            'hpos-seed-receive=hpos_seed.receive_cli:main',
            'hpos-seed-send=hpos_seed.send_cli:main',
            'hpos-seed-send-qt=hpos_seed.send_qt:main'
        ],
    },
    package_data={'hpos_seed': ['send_qt.qml']},
    include_package_data=True,
    install_requires=['magic-wormhole']
)
