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
    merged_data = []

    for idx_cbpm in range(config.n_cbpm):

        print(' <<<<                     >>>>')
        print(' <<<< Analyzing CBPM:', config.cbpm[idx_cbpm], '>>>>')
        print(' <<<<                     >>>>')

        raw_data.append([])
        button_data.append([])
        
        for idx_file in range(config.n_data_file):
            
            raw_data[idx_cbpm].append(dataparser.DataParser(config, config.data_file[idx_file], config.cbpm[idx_cbpm]))
            raw_data[idx_cbpm][idx_file].parse_main_header()
            raw_data[idx_cbpm][idx_file].extract_single_cbpm_data()
            merged_data[idx_cbpm] += raw_data[idx_cbpm][0].self.button[0] + raw_data[idx_cbpm][1].self.button[0]

            button_data[idx_cbpm].append(button.Button(raw_data[idx_cbpm][idx_file]))
            button_data[idx_cbpm][idx_file].extract_button_information()
            button_data[idx_cbpm][idx_file].calculate_vertical_centroid()
            button_data[idx_cbpm][idx_file].calculate_horizontal_centroid()
#            button_data[idx_cbpm][idx_file].button_fft()


merged_data = raw_data[idx_cbpm][0].self.button[0] + raw_data[idx_cbpm][1].self.button[0]




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
