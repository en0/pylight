from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.readlines()

with open('README.md', "r") as f:
    long_description = f.read()

setup(
    name='pylight',
    version='1.0.0',
    author='Ian Laird',
    author_email='irlaird@gmail.com',
    url='https://github.com/en0/pylight',
    keywords=['backlight'],
    description='Backlight Control',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=['pylight'],
    entry_points={
        'console_scripts': [
            'pylightd = pylight.pylightd:main',
            'pylightctl = pylight.pylightctl:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
)
