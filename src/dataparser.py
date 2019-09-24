import src.configparser as configparser
import re
import sys
import numpy as np

# class that parses the data file to extract
# the per-button information

class DataParser(configparser.ConfigParser):

    def __init__(self, config, data_file, cbpm):
        self.data_file = data_file
        self.cbpm = cbpm
        self.config = config
        self.n_turns = -1
        self.raw_data = []

    def check_input_file(self, data_file):
            try:
                file_object = open(data_file, 'r')
                if (self.config.verbose > 0 ):
                    print('\n Input text file ', data_file, 'opened succesfully')
            except:
                print('ERROR -- could not open file: ', data_file)	
                sys.exit(0)

    def parse_main_header(self):

        self.check_input_file(self.data_file)

        file_object = open(self.data_file, 'r')

        # retrieve number of turns
        for line in file_object:
            if re.search('Number_of_Turns', line):
                split_line = line.split()
                self.n_turns = int(split_line[2])
                if (self.config.verbose > 0 ):
                    print(' Number of turns: ', self.n_turns)
                break

    def extract_single_cbpm_data(self):

        file_object = open(self.data_file, 'r')

        analyze_data = False
        count_header = False
        header_counter = 0
        turn_counter = 0

        # retrieve buttons information from a given CBPM
        for line in file_object:

            if (analyze_data and turn_counter < self.n_turns):
                turn_counter += 1
                if (self.config.verbose > 1):
                    print(turn_counter)
                split_line = line.split()
                self.raw_data.append([int(split_line[idx]) for idx in range(2,6)])
            elif re.search('Location', line):
                split_line = line.split()
                if (split_line[2] == self.cbpm):
                    if (self.config.verbose > 0 ):
                        print(' Found data for CBPM: ', self.cbpm)
                    count_header = True

            if (count_header):
                header_counter += 1

            if (header_counter == 31 and re.search('--BEGIN DATA--', line)):
                analyze_data = True

        self.raw_data = np.array(self.raw_data)
