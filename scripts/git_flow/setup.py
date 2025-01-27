from setuptools import setup, find_packages

setup(
    name='git-flow',
    version='0.1.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'git-flow=git_flow.cli:main',
        ],
    },
    install_requires=[],
    python_requires='>=3.6',
)
