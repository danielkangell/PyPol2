#!/usr/bin/env python -i
# preceding line should have path for Python on your machine

# Argon_melt_0p.py
# Purpose: mimic operation of examples/COUPLE/simple/simple.cpp via Python

# Serial syntax: Argon_melt_0p.py in_example.lammps
#                in_example.lammps = LAMMPS input script

# Parallel syntax: mpirun -np 4 Argon_melt_0p.py in_example.lammps
#                  in_example.lammps = LAMMPS input script
# also need to uncomment either Pypar or mpi4py sections below

from __future__ import print_function
import sys
import numpy as np
import ctypes

# parse command line

argv = sys.argv
if len(argv) != 2:
  print("Syntax: Argon_melt_0p.py in_example.lammps")
  sys.exit()

infile = sys.argv[1]

me = 0


# uncomment this if running in parallel via mpi4py
from mpi4py import MPI
me = MPI.COMM_WORLD.Get_rank()
nprocs = MPI.COMM_WORLD.Get_size()

from lammps import PyLammps
lmp = PyLammps()

# run infile one line at a time

# my in.lammps file has a run command as the last step, so modify this and it also has a dump
lines = open(infile,'r').readlines()
for line in lines: lmp.command(line)

# run 10 more steps
# get coords from LAMMPS
# change coords of 1st atom
# put coords back into LAMMPS
# run a single step with changed coords

lmp.command("run 10")
