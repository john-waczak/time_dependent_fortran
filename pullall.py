#!usr/bin/python3

import os 

researchers = ['john-waczak', 'ionizationcalc']

for researcher in researchers:
	os.system("git pull git://github.com/{}/time_dependent_fortran.git :".format(researcher))

