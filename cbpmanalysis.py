import src.configparser as configparser
import src.dataparser as dataparser
import src.button as button
import src.printout as printout
import sys

def main():

    # retrieve configuration file information
    config = configparser.ConfigParser()
    config.parse_config()
    config.check_config()

    raw_data = []
    button_data = []
    for idx_cbpm in range(config.n_cbpm):

        print('\n Analyzing CBPM: ', config.cbpm[idx_cbpm], '\n')

        if (config.merge_data_file):

            raw_data.append(dataparser.DataParser(config))
            raw_data[idx_cbpm].parse_main_header()
            raw_data[idx_cbpm].extract_single_cbpm_data(config.cbpm[idx_cbpm])

            button_data.append(button.Button(raw_data[idx_cbpm]))
            button_data[idx_cbpm].extract_button_information()
            button_data[idx_cbpm].calculate_vertical_centroid()




if __name__ == '__main__':

    # print welcome message
    printout.print_welcome_message()

    # check that the configuration file was provided
    # exit if not provided
    if len(sys.argv) < 2:
        print(' RUNNING ERROR -- configuration file must be provided via command line argument')
        sys.exit(0)

    # run the analysis for associated configuration file
    sys.exit(main())
