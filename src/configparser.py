import json
import sys
from pprint import pprint


# read in configuration file

class ConfigParser:

    def parse_config(self):

        with open(sys.argv[1]) as config_file:
            config = json.load(config_file)

        self.data_file = config['data_file'].split()
        self.n_data_file = config['n_data_file']
        self.verbose = int(config['verbose'])
        self.cbpm = config['cbpm'].split()
        self.n_cbpm = config['n_cbpm']
        self.analysis_type = config['analysis_type']
        self.kx = config['kx']
        self.ky = config['ky']
        self.boxcar_avg = int(config['boxcar_avg'])
        self.apply_boxcar_avg = config['apply_boxcar_avg']
        self.pedestal_correction = config['pedestal_correction']

        self.create_data_file_tag()

    def create_data_file_tag(self):
        self.data_file_tag = []
        for i in range(len(self.data_file)):
            self.data_file_tag.append(self.data_file[i][5:len(self.data_file[i]) - 4])


    def check_config(self):

        if self.verbose > 2:
            self.dump()
        if self.n_cbpm != len(self.cbpm):
            print('   CONFIGURATION ERROR -- Mismatch between thee number of CBPM provided and the expected number')
            sys.exit(0)
        if self.n_data_file != len(self.data_file):
            print(
                '   CONFIGURATION ERROR -- Mismatch between thee number of file(s) provided ("data_file") '
                'and the expected number ("n_data_file")')
            sys.exit(0)

    def dump(self):
        pprint(vars(self))
