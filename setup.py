from setuptools import setup, find_packages

setup(
    name='axabsent',
    version='0.1.0',
    description='AxAbsEnt Causal Scheduler and Recursive Execution Engine',
    author='RJV Technologies Ltd',
    packages=find_packages(),
    install_requires=[
        "tensorflow>=2.14.0",
        "numpy>=1.24.0",
        "tqdm>=4.64.0"
    ],
    entry_points={
        'console_scripts': [
            'axabsent-scheduler=umg.cycle2.scheduler:main'
        ]
    },
    python_requires='>=3.8'
)