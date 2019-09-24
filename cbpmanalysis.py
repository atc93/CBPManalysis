# standard library imports
import sys

# local application imports
import src.printout as printout
from src.analyze import Analyze
from src.configparser import ConfigParser
from src.dataparser import DataParser


def main():
    # retrieve configuration file information
    config = ConfigParser()
    config.parse_config()
    config.check_config()

    raw_button_data = []
    analyze = []

    for idx_cbpm in range(config.n_cbpm):

        printout.analyzed_cbpm(config.cbpm[idx_cbpm])

        raw_button_data.append([])
        analyze.append([])

        for idx_file in range(config.n_data_file):
            raw_button_data[idx_cbpm].append(DataParser(config, idx_file, idx_cbpm))
            raw_button_data[idx_cbpm][idx_file].parse_main_header()
            raw_button_data[idx_cbpm][idx_file].extract_single_cbpm_data()

            analyze[idx_cbpm].append(Analyze(raw_button_data[idx_cbpm][idx_file], config, idx_file))
            analyze[idx_cbpm][idx_file].raw_button_information()
            analyze[idx_cbpm][idx_file].vertical_centroid()
            analyze[idx_cbpm][idx_file].horizontal_centroid()


if __name__ == '__main__':

    # print welcome message
    printout.welcome_message()

    # check that the configuration file was provided
    # exit if not provided
    if len(sys.argv) < 2:
        print(' RUNNING ERROR -- configuration file must be provided via command line argument')
        sys.exit(0)

    # run the analysis for associated configuration file
    sys.exit(main())
