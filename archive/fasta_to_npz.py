#!/usr/bin/env python

# This code extracts the sequences in fasta files and stores them in a numpy
# binary archive
#
# To execute this code run
# fasta_to_npz.py <output_file> <input_file1> <input_file2> ...
#
# parameters :
# - output_file : name of the file to write in
# - input_file : fasta files from which to extract data, must be in typical
#       | info     | format
#       | sequence |
#       if multiple input files are given, all the sequences are
#       stored in the same array

import sys
import numpy as np
from pathlib import Path

# Get the arguments from the command line and handle exceptions
try:
    output_file = sys.argv[1]
except IndexError as ie:
    raise SystemError("Error: Specify output file as 'fastq_to_npz.py "
                      "<output_file> <input_file1> <input_file2> ...'\n")

try:
    input_file = sys.argv[2]
except IndexError as ie:
    raise SystemError("Error: Specify at least one input file as "
                      "'fastq_to_npz.py <output_file> <input_file1> "
                      "<input_file2> ...'\n")

# loop over input files to check if they exist
cur_arg = 2
while cur_arg < len(sys.argv):
    if not Path(sys.argv[cur_arg]).is_file():
        raise SystemError("Error: File ", sys.argv[cur_arg],
                          " does not exist\n")
    cur_arg += 1

# loop over input files to extract sequences
cur_arg = 2
while cur_arg < len(sys.argv):
    # list of all sequences
    reads = []
    with open(sys.argv[cur_arg], 'r') as f:
        # loop over file lines
        read = ''
        for line in f:
            if line[0] == '>':  # First line header, discard this line
                if read != '':
                    reads.append(read)  # add completed read
                    read = ''
            else:
                read += line.rstrip()  # remove space at the end
    reads.append(read)  # add last read
    cur_arg += 1
reads = np.array(reads)
# convert the list to array and store in a numpy binary file
np.savez_compressed(output_file,
                    reads=reads)
