import sys 
import json

# read in configuration file

class ConfigParser:

    def parse_config(self):
        with open(sys.argv[1]) as config_file:
            config = json.load(config_file)
        self.data_file = config['data_file'].split()
        self.verbose = int(config['verbose'])
        self.cbpm = config['cbpm'].split()
        self.n_cbpm = config['n_cbpm']
        self.analysis_type = config['analysis_type']
        self.kx = config['kx']
        self.ky = config['ky']
        self.merge_data_file = config['merge_data_file']

    def check_config(self):
#        if (self.analysis_type == 'single' and len(self.cbpm) != 1):
#            print(' CONFIGURATION ERROR -- Expect only 1 CBPM for a single CBPM analysis')
#            sys.exit(0)
        if (self.n_cbpm != len(self.cbpm)):
            print(' CONFIGURATION ERROR -- Mismatch between thee number of CBPM provided and the expected number')
            sys.exit(0)

