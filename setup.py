from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy
import os


ext = [
        Extension(name="artery.matlaws._artery",
          sources=["src/cython/artery.pyx"],
          include_dirs=[numpy.get_include(), os.path.dirname(__file__)],
          extra_compile_args=['-Ofast', "-flto", "-march=native", "-std=c++17"],
        ),
      ]

setup(ext_modules=cythonize(ext, build_dir="src/cython/build"))
