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
./build.sh
```

Then cd to the notebooks subfolder and explore the jupyter notebooks:

```
cd notebooks
```

## Supported Options

### Fortran Compiler

If you have no fortran installed, you have two options.
First, you can install GNU Fortran:

```
sudo apt update
sudo apt install gfortran -y
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


