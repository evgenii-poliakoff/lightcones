import setuptools
from numpy.distutils.core import setup, Extension
from configparser import ConfigParser
import warnings

# Determine what fortran compiler is chosen by the user
# initialize a ConfigParser object
config = ConfigParser()
# read the setup.cfg file
config.read('setup.cfg')
# access the fcompiler value from the [build_ext] section
fcompiler = config.get('build_ext', 'fcompiler')
# access the [$fcompiler]_options value from the [build_ext] section
fcompiler_options = config.get('user_options', fcompiler + '_options')
fcompiler_options = fcompiler_options.split()

# Define the Fortran extensions
_fastmul = Extension(
    name='lightcones.linalg._fastmul',  
    sources=['src/lightcones/linalg/fastmul.f90'],
    extra_f90_compile_args=fcompiler_options
)

_dlancz = Extension(
    name='lightcones.linalg._dlancz',  
    sources=['src/lightcones/linalg/dlancz.f'],
    extra_f77_compile_args=fcompiler_options
)

_solve = Extension(
    name='lightcones.solvers.schrodinger._solve',  
    sources=['src/lightcones/solvers/schrodinger/solve.f90'],
    extra_f90_compile_args=fcompiler_options
)

_outer = Extension(
    name='lightcones._outer',  
    sources=['src/lightcones/outer.f90'],
    extra_f90_compile_args=fcompiler_options
)

# Set up the configuration
config = {
    'name': 'lightcones',
    'version': '0.1',
    'description': 'Light cones package for real-time quantum impurity quenches',
    'ext_modules': [_fastmul, _dlancz, _solve, _outer],
    'packages': ['lightcones'],
    'package_dir': {'lightcones': 'lightcones'},
    'install_requires': [],
    'zip_safe': False,
}

# Run the setup
setup(**config)