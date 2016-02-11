from setuptools import setup

setup(
    name='yandex-geocoder',
    version='0.0.1',
    description='Client for Yandex geocoding service',
    author='Alexander Tihonruk',
    author_email='atihonruk@gmail.com',
    url='https://gist.github.com/atihonruk/822273c3a196b90a2b60',
    py_modules=['geocode'],
    install_requires=['requests']
)
