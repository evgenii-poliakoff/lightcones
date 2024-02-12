import setuptools
from numpy.distutils.core import setup, Extension

# Define the Fortran extensions
_fastmul = Extension(
    name='lightcones.linalg._fastmul',  
    sources=['src/lightcones/linalg/fastmul.f90'],
    extra_f90_compile_args=['-fast']
)

_solve = Extension(
    name='lightcones.solvers.schrodinger._solve',  
    sources=['src/lightcones/solvers/schrodinger/solve.f90'],
    extra_f90_compile_args=['-fast']
)

# Set up the configuration
config = {
    'name': 'lightcones',
    'version': '0.1',
    'description': 'Light cones package for real-time quantum impurity quenches',
    'ext_modules': [_fastmul, _solve],
    'packages': ['lightcones'],
    'package_dir': {'lightcones': 'lightcones'},
    'install_requires': [],
    'zip_safe': False,
}

# Run the setup
setup(**config)