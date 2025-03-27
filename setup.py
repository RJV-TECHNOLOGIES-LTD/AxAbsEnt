from setuptools import setup, find_packages

setup(
    name='AxAbsEnt',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'axabsent=AxAbsEnt.ai_system.core_agent:main',
        ]
    },
)
