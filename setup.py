from setuptools import setup

setup(
    name='keycloak-python',
    version='0.1',
    description='HTTP server agnostic library to support authentication and authorization with keycloak.',
    url='https://github.com/ibotty/keycloak-python',
    author='Tobias Florek',
    author_email='tob@butter.sh',
    packages=[
        'keycloak',
        'keycloak.http_api',
        'keycloak.store'
    ],
    install_requires=[
       'python-jose>=1.3.2'
    ]
)