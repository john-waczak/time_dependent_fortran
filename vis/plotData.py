#!/user/bin/env python3

import numpy as np
import argparse
import os, sys 
import matplotlib.pyplot as plt
from scipy.io import FortranFile
from matplotlib import animation


# set up the command line parser

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

parser.add_argument('-d', '--datafile', action="store", type=str, help='Data file you would like to visualize')

group.add_argument('-m', '--movie', action="store_true", default=False, help='Whether or not you want to make a movie')

group.add_argument('-g', '--graph', action="store_true", default=True, help='Wheter or not you want to make a graph')

parser.add_argument('-n', '--atomicNumber', action="store", type=int, default=26, help="Atomic number for element ion fractiosn you want to graph")

parser.add_argument('-f', '--filename', action="store", type=str, default="graph", help="Name for output file. Ex: graph would be saved to graph.png or graph.mp4")

parser.add_argument('-i', '--interactive', action="store_true", default=False, help="Choose to entery matplotlib's interactive graph viewer")

args = parser.parse_args()



try:
    f = FortranFile(args.datafile, 'r')
except:
    raise SystemExit

# read in starting/ending temperature and density
[te_sta, te_end, ne] = f.read_reals(dtype=np.float64)

fraction_initial = f.read_reals(dtype=np.float64).reshape(30,30)
fraction_end = f.read_reals(dtype=np.float64).reshape(30,30)

# read total number of time steps 
n_timeSteps = f.read_ints()

times = []
fractions = []

# add in the first set as well as t=0
times.append(0.0)
fractions.append(fraction_initial)

# loop through data and append to lists
for i in range(n_timeSteps[0]):  # read_ints() reads as arrays so we have to index it
    time = f.read_reals(dtype=np.float64)
    current_fractions = f.read_reals(dtype=np.float64).reshape(30,30)
    times.append(time[0])
    fractions.append(current_fractions)

# add final set
fractions.append(fraction_end)
times.append(np.abs(times[-1]-times[-2]))




if (args.graph is True):
    plt.figure()
    plt.yscale("log")
    plt.ylim(1.0e-5, 1.0)
    plt.xlabel("Charge states")
    plt.ylabel("Ion fractions for element {}".format(args.atomicNumber))

    charge_states = np.linspace(1, args.atomicNumber+1, args.atomicNumber+1)

    #plot the first and last one in bold
    plt.plot(charge_states, fractions[0][args.atomicNumber-1, 0:args.atomicNumber+1], c='b', label="T_sta")
    plt.plot(charge_states, fractions[-1][args.atomicNumber-1, 0:args.atomicNumber+1],c='r', label="T_end")

    for i in range(1, len(fractions)-1):
        plt.plot(charge_states, fractions[i][args.atomicNumber-1, 0:args.atomicNumber+1], c='k', alpha=0.4)
    plt.legend()
    if (args.interactive is True):
        plt.show()
    plt.savefig(args.filename)


if (args.movie is True):
    if not os.path.isdir(args.filename):
        os.mkdir(args.filename)
    os.chdir(args.filename)
    print(os.getcwd())


    for i in range(len(fractions)):
        print(i) 
        plt.figure()
        plt.yscale("log")
        plt.xlabel("Charge states")
        plt.ylabel("Ion fractions for element {}".format(args.atomicNumber))
        plt.ylim(1.0e-5, 1.0) 

        charge_states = np.linspace(1, args.atomicNumber+1, args.atomicNumber+1)

        plt.plot(charge_states, fractions[i][args.atomicNumber-1, 0:args.atomicNumber+1], c='k')

        plt.savefig(args.filename+"-{0:04d}".format(i)+".png")
        plt.close()

    os.system("ffmpeg -i {}-%-4d.png ../{}.mp4".format(args.filename, args.filename)) 
    os.system("rm *.png")
































