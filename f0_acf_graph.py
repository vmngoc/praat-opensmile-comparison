# Python script for reading f0 data from .csv files and plotting f0 data over time for all sound files in a directory

import os
import re
from matplotlib import pyplot as plt
import pylab as pylab
import numpy as np

# set up path to the directories containing f0 data 
current_dir = os.getcwd()
data_dir = os.path.abspath(os.path.join(current_dir, os.pardir,'f0_data'))
praat_dir = os.path.join(data_dir,'Praat/acf')
os_dir = os.path.join(data_dir,'openSMILE/acf')
saved_dir = os.path.join(current_dir, 'acf')

# read from the text file containing list of .wav files to analyze
f = open('../sounds/files_to_analyze.txt', 'r')
for filepath in f:
	# get rid of file extension
	soundname = os.path.splitext(filepath)[0] 

	# get data from csv files (the first column contains the timestamp, the second column contains f0 values)
	praat_data = np.genfromtxt(os.path.join(praat_dir, soundname+'_f0_praat.csv' ), delimiter = ',', skiprows=1, usecols=(1,2), unpack=True)
	opensmile_data = np.genfromtxt(os.path.join(os_dir, soundname+'-prosodyAcf.csv'), delimiter = ';', skiprows=1, usecols=(1,2), unpack=True)
	
	# process openSMILE data so that all values under 75 are eliminated (since minimum setting for f0 in Praat is 50)
	opensmile_data = opensmile_data[:,opensmile_data[1]>=75]

	# generate scatter graph
	open_smile = plt.scatter(opensmile_data[0],opensmile_data[1], s=3, color='blue')
	praat = plt.scatter(praat_data[0],praat_data[1], s=3, color='red')

	# put label and legend on the graph
	plt.title('Fundamental frequency for file ' + soundname)
	plt.ylabel('F0 Mean')
	plt.xlabel('Time (seconds)')
	plt.legend((praat, open_smile),
	           ('Praat data', 'openSMILE data'),
	           scatterpoints=1,
	           loc='upper right',
	           ncol=3,
	           fontsize=12)

	# save as PNG image 
	pylab.savefig(os.path.join(saved_dir, soundname)+'.png', bbox_inches='tight')
	plt.clf() # clear figure before next loop
