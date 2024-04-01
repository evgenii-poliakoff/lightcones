# lightcones

This repository holds the python packages for the generalized light cone approach to the problem of out-of-equilibrium dynamics of quantum impurities  

## Getting started

Clone the repository:

```
git clone https://github.com/evgenii-poliakoff/lightcones.git
cd lightcones
```

Install the requirements:

```
./scripts/install_requirements.sh
```

Build the package:

```
python3 setup.py develop
```

Then cd to the tutorials subfolder and explore the jupyter notebooks:

```
cd tutorials
```

## Supported Options

### Fortran Compiler

If you have no fortran installed, you have two options.
First, you can install GNU Fortran:

```
sudo apt update
sudo apt install gfortran -y
```

However, this requires administrative priveleges. 

If you need to install fortran for local user (e.g. on a server account without root access), you can install Intel Fortran Compiler, which is free for non-commercial use. For this purpose, set the fcompiler option to "intelem" in setup.cfg file:

```
[build_ext]
fcompiler=intelem
```

Then run

```
./scripts/install_requirements.sh
```

again. The necessary dependencies will be automatically downloaded. Then build the package

```
python3 setup.py develop
```

### Python distribution

If your have some problems with your python distribution, you can install locally (without root access) Anaconda3 python distribution which contains everything needed for scientific computing out-of-box. For this purpose, set the install_anaconda  option to "yes" in setup.cfg file:

```
[user_options]
install_anaconda=yes
```

Then run

```
./scripts/install_requirements.sh
```

again. The necessary dependencies will be automatically downloaded. Then build the package

```
./build.sh
```


