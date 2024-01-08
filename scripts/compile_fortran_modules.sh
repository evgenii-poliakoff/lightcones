#! /bin/sh
echo "Current directory: $(pwd)"
cd ./src
python3 -m numpy.f2py --quiet -c fastmul.f90 -m fastmul --fcompiler=intelem --f90flags=-fast
python3 -m numpy.f2py --quiet -c evolution_chained2.f90 -m evolution_chained2  --fcompiler=intelem --f90flags=-fast
python3 -m numpy.f2py --quiet -c evolution_chained2_kicked.f90 -m evolution_chained2_kicked  --fcompiler=intelem --f90flags=-fast
python3 -m numpy.f2py --quiet -c evolution.f90 -m evolution  --fcompiler=intelem --f90flags=-fast
python3 -m numpy.f2py --quiet -c evolution2.f90 -m evolution2  --fcompiler=intelem --f90flags=-fast
python3 -m numpy.f2py --quiet -c local_op.f90 -m local_op --fcompiler=intelem --f90flags=-fast