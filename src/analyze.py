from src.dataparser import DataParser
import src.constants as constants
import matplotlib.pyplot as plt
import src.plotting as plotting
import numpy as np

class Analyze(DataParser):

    def __init__(self, raw_button, config, idx_file):
        self.raw_button = raw_button
        self.config = config
        self.button_sum = []
        self.button = []
        self.std_button = []
        self.mean_button = []
        self.idx_file = idx_file

    def raw_button_information(self):
        # extract individual buttons information
        # button 0 (or 3) is inner top
        # botton 1 (or 1) is inner bottom
        # bottom 2 (or 2) is outter bottom
        # button 3 (or 4)is outter top
        if (self.config.verbose > 0):
            print('\n ---------------------')
            print(' | Raw button values |')
            print(' ---------------------\n')

        for i in range(4):
            self.button.append(self.raw_button.data[:,i])
            if (self.config.verbose > 0):
                print(' Button #', i)
                for boxcar_averaging_window in (1, 2, 4, 8, 16, 32, 64, 128):
                    data = self.boxcar_averaging(np.array(self.button[i]), boxcar_averaging_window)
                    print(' boxcar ', boxcar_averaging_window, ' -- mean: {0:0.2f} ADU'.format(np.mean(data)), 
                        ', std: {0:0.2f} ADU'.format(np.std(data))
                        , ', std/mean: {0:0.5f}'.format(np.std(data)/np.mean(data)))
            self.perform_fft(np.array(self.button[i]), 'button ' + str(i), 'button_' + str(i))

        self.button_sum = self.button[0]+self.button[1]+self.button[2]+self.button[3]


    @staticmethod
    def boxcar_averaging(data, averaging_window):
        
        n_steps = int(len(data)/averaging_window)
        boxcar_data = np.zeros((n_steps))
        for i in range(n_steps):
            boxcar_data[i] = np.mean(data[i*averaging_window:(i+1)*averaging_window], axis=0)

        return boxcar_data
            

    def perform_fft(self, data, title, label):

        for boxcar_averaging_window in (1, 16, 32, 64, 128):
            
            #fft_data = self.boxcar_averaging(np.array(data), boxcar_averaging_window)
            fft_data = self.boxcar_averaging(data, boxcar_averaging_window)
            fft = np.abs(np.fft.fft(fft_data))
            fft = fft[range(1, int(len(fft)/2))] # exclude the 0 Hz bin and the mirror symmetry data points
            
            freq_step = 1/(len(data)*constants.ring_revolution_period) # keep sample period to revolution
            frequencies = [int(i)*freq_step/1000 for i in range(0, len(fft))] # in from Hz to kHz
            
            boxcar_title = title +'\nboxcar ' + str(boxcar_averaging_window)
            fig, ax = plotting.create_figure(boxcar_title, 'Frequency [kHz]', 'FFT magnitude (log base 10)', label)
            ax.set_yscale('log')
            ax.set_xlim(frequencies[0], frequencies[len(frequencies)-1])

            plt.grid(color='black', linestyle=':', linewidth=0.5, alpha=0.1)
            plt.grid(True)
            plt.plot(frequencies, fft)
            plt.savefig('results/'+self.config.data_file[self.idx_file][5:len(self.config.data_file[self.idx_file])-4]+'_' + label + '_boxcar' + str(boxcar_averaging_window) + '.eps')
            plt.close()
        

    def vertical_centroid(self):
        self.vertical_centroid = []
        for i in range(self.config.n_turns):
            self.vertical_centroid.append(self.config.ky*(self.button[0][i]+self.button[3][i]-(self.button[1][i]+self.button[2][i]))/self.button_sum[i])
        self.mean_vertical_centroid =  np.mean(self.vertical_centroid)
        self.std_vertical_centroid =  np.std(self.vertical_centroid)
        self.perform_fft(self.vertical_centroid, 'vertical centroid', 'vertical_centroid')
        if (self.config.verbose > 0 ):
            print('\n ---------------------')
            print(' | Vertical centroid |')
            print(' ---------------------\n')        
            print(' y = {0:0.2f}'.format(self.mean_vertical_centroid), ' +- {0:0.2f}'.format(self.std_vertical_centroid), '(std) mm')

    def horizontal_centroid(self):
        self.horizontal_centroid = []
        for i in range(self.config.n_turns):
            self.horizontal_centroid.append(self.config.kx*(self.button[2][i]+self.button[3][i]-(self.button[1][i]+self.button[0][i]))/self.button_sum[i])
        self.mean_horizontal_centroid =  np.mean(self.horizontal_centroid)
        self.std_horizontal_centroid =  np.std(self.horizontal_centroid)
        self.perform_fft(self.horizontal_centroid, 'horizontal centroid', 'horizontal_centroid')
        if (self.config.verbose > 0 ):
            print('\n -----------------------')
            print(' | Horizontal centroid |')
            print(' -----------------------\n')        
            print(' x = {0:0.2f}'.format(self.mean_horizontal_centroid), ' +- {0:0.2f}'.format(self.std_horizontal_centroid), '(std) mm')