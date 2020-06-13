# setuptools loads some plugins necessary for use here.
from setuptools import find_packages  # noqa: F401
from distutils.core import setup

# Use the readme as the long description.
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="make-it-sync",
      version='1.0.0',
      packages=['make_it_sync'],
      scripts=[],
      description="Create a sync version of an async function",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="G. Watts (IRIS-HEP/UW Seattle)",
      author_email="gwatts@uw.edu",
      maintainer="Gordon Watts (IRIS-HEP/UW Seattle)",
      maintainer_email="gwatts@uw.edu",
      url="https://github.com/gordonwatts/make-it-sync",
      license="MIT",
      python_requires='>=3.6',
      test_suite="tests",
      install_requires=[
      ],
      extras_require={
          'test': [
              'pytest>=3.9',
              'pytest-asyncio',
              'pytest-mock',
              'pytest-cov',
              'coverage',
              'flake8',
              'codecov',
              'autopep8',
              'twine',
              'wheel'
          ],
      },
      classifiers=[
          "Development Status :: 3 - Alpha",
          # "Development Status :: 4 - Beta",
          # "Development Status :: 5 - Production/Stable",
          # "Development Status :: 6 - Mature",
          "Intended Audience :: Developers",
          "Intended Audience :: Information Technology",
          "Programming Language :: Python",
          "Topic :: Software Development",
          "Topic :: Utilities",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
      ],
      platforms="Any",
      )
