from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ddd-cli',
    version='1.3.12',
    description='CLI para agregar soporte DDD a proyectos Python/Django',
    long_description=long_description,
    long_description_content_type="text/markdown",      
    author='Ragnar Bermúdez La O',
    author_email='ragnarbermudezlao@gmail.com',
    packages=find_packages(),
    install_requires=['django', 'jinja2'],
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
