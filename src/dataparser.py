from src.configparser import ConfigParser
import re
import sys
import numpy as np

# class that parses the data file to extract
# the per-button information

class DataParser(ConfigParser):

    def __init__(self, config, idx_file, idx_cbpm):
        self.config = config
        self.data_file = config.data_file[idx_file]
        self.cbpm = config.cbpm[idx_cbpm]
        self.data = []

    def check_input_file(self):
            try:
                open(self.data_file, 'r')
                print('\n Input text file ', self.data_file, 'opened successfully')
            except:
                print('ERROR -- could not open file: ', self.data_file)
                sys.exit(0)

    def parse_main_header(self):

        self.check_input_file()

        file_object = open(self.data_file, 'r')

        # retrieve number of turns
        for line in file_object:
            if re.search('Number_of_Turns', line):
                split_line = line.split()
                self.config.n_turns = int(split_line[2]) # add n_turns information to the config object
                if (self.config.verbose > 0 ):
                    print(' Number of turns: ', self.config.n_turns)
                break

        file_object.close()

    def extract_single_cbpm_data(self):

        file_object = open(self.data_file, 'r')

        analyze_data: bool = False
        count_header = False
        header_counter = 0
        turn_counter = 0

        # retrieve buttons information for a given CBPM
        for line in file_object:

            if (analyze_data and turn_counter < self.config.n_turns):
                turn_counter += 1
                if (self.config.verbose > 3):
                    print(turn_counter)
                split_line = line.split()
                self.data.append([int(split_line[idx]) for idx in range(2,6)])
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

        file_object.close()

        self.data = np.array(self.data)

