from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ddd-cli',
    version='1.3.20',
    description='CLI for adding DDD support to Python/Django projects',
    long_description=long_description,
    long_description_content_type="text/markdown",      
    author='Ragnar Bermúdez La O',
    author_email='ragnarbermudezlao@gmail.com',
    packages=find_packages(),
    include_package_data=True,  
    install_requires=['django', 'jinja2', 'colorama'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    entry_points={
        'console_scripts': [
            'ddd = ddd.management.cli:main',  # Registra el comando `ddd`
        ],
    },
)
