from setuptools import setup

setup(
    name="ricardo_codex",
    version="1.0.0",
    description="Recursive Identity Verification and Codex Decoder for Ω₅–Ω∞ epochs",
    author="Ricardo Jorge do Vale",
    py_modules=["ricardo_codex"],
    entry_points={
        'console_scripts': ['codex-decode=ricardo_codex:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)