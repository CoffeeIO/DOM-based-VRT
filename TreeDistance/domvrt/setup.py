from setuptools import setup

setup(name='domvrt',
      version='0.1',
      description='',
      url='https://github.com/MGApcDev/DOM-based-VRT',
      author='MGApcDev',
      author_email='mgapcdev@gmail.com',
      license='GNU General Public License v3.0',
      packages=['domvrt'],
      install_requires=[
          'six',
          'lorem',
          'yattag',
          'image',
          'selenium',
          'time'
      ],
      zip_safe=False)
