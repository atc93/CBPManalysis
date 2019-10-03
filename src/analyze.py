from src.dataparser import DataParser
import src.constants as constants
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import src.plotting as plotting
import src.util as util
import src.printout as printout
import numpy as np
import math
from scipy.optimize import curve_fit

class Analyze(DataParser):

    def __init__(self, raw_button, config, idx_file, idx_cbpm):
        self.raw_button = raw_button
        self.config = config
        self.button_sum = []
        self.button = []
        self.std_button = []
        self.mean_button = []
        self.idx_file = idx_file
        self.idx_cbpm = idx_cbpm

    def raw_button_information(self):
        # extract individual buttons information
        # button 0 (or 3) is inner top
        # botton 1 (or 1) is inner bottom
        # bottom 2 (or 2) is outter bottom
        # button 3 (or 4)is outter top
        if (self.config.verbose > 0):
            print('\n   ---------------------')
            print('   | Raw button values |')
            print('   ---------------------\n')

        for i in range(4):

            self.button.append(self.raw_button.data[:,i])

            if (self.config.verbose > 0):
                print('   Button #', i, '--', end='')

            for j in range (self.config.boxcar_avg_maxpow2+1):
                boxcar_averaging_window = int(math.pow(2, j))
                data = self.boxcar_averaging(np.array(self.button[i]), boxcar_averaging_window)
                self.mean_button.append(np.mean(data))
                self.std_button.append(np.std(data))
                printout.print_stat(data)

                # plot raw button reading distribution
                boxcar_title = str(self.config.cbpm[self.idx_cbpm]) + ' button ' + str(i) + '\nboxcar ' + str(boxcar_averaging_window)
                label = 'button' + str(i)
                fig, ax = plotting.create_figure(boxcar_title, 'Button raw readings [ADU]', '#', self.config.data_file_tag[self.idx_file], self.config.timestamp)
                intensity, bin_edge, _ = plt.hist(data, bins=int(math.sqrt(len(data))))
                bin_center = (bin_edge[:-1]+bin_edge[1:])/2.
                popt, pcov = curve_fit(util.double_gauss_func, bin_center, intensity, p0=[max(intensity), np.mean(data)+np.std(data)/2, np.std(data)/2,
                                                                                          max(intensity)/2, np.mean(data)-np.std(data)/2, np.std(data)/2])
                plt.plot(bin_center, util.double_gauss_func(bin_center, *popt), color='red', linewidth=2.5)
                plt.plot(bin_center, util.gauss_func(bin_center, *popt[0:3]), ls='--', color='darkorange', linewidth=2)
                plt.plot(bin_center, util.gauss_func(bin_center, *popt[3:6]), ls='--', color='darkorange', linewidth=2)
                #print(math.sqrt(popt[2]**2+popt[5]**2), (popt[0]*popt[1]+popt[3]*popt[4])/(popt[0]+popt[3]))
                plt.savefig('results/' + self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + label + '_boxcar' + str(
                    boxcar_averaging_window) + '_rawADU.eps')
                plt.close()

                # plot raw button reading as a function of turn #
                fig, ax = plotting.create_figure(boxcar_title, 'Turn #', 'Button reading [ADU]', self.config.data_file_tag[self.idx_file], self.config.timestamp)
                plt.plot([i for i in range(len(data))], data)
                plt.savefig('results/' + self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + label + '_boxcar' + str(
                    boxcar_averaging_window) + '_rawADUtrend.eps')
                plt.close()

                # plot mean subtracted raw button reading as a function of turn #
                fig, ax = plotting.create_figure(boxcar_title, 'Turn #', 'Button reading [ADU]', self.config.data_file_tag[self.idx_file], self.config.timestamp)
                plt.plot([i for i in range(len(data))], data-np.mean(data))
                plt.savefig('results/' + self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + label + '_boxcar' + str(
                    boxcar_averaging_window) + '_rawADUtrendAvgSubtracted.eps')
                plt.close()

            self.perform_fft(np.array(self.button[i]), 'button ' + str(i), 'button_' + str(i))

        self.button_sum = self.button[0]+self.button[1]+self.button[2]+self.button[3]

        self.button_cross = ((self.button[0]+self.button[2]) - (self.button[1]+self.button[3]))/self.button_sum
        # plot button cross reading distribution
        fig, ax = plotting.create_figure(boxcar_title, 'Button cross reading [ADU]', '#',
                                         self.config.data_file_tag[self.idx_file], self.config.timestamp)
        plt.hist(self.button_cross, bins=int(math.sqrt(len(self.button_cross))))
        plt.savefig('results/' + self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + 'Button_cross.eps')
        plt.close()


    @staticmethod
    def boxcar_averaging(data, averaging_window):
        
        n_steps = int(len(data)/averaging_window)
        boxcar_data = np.zeros((n_steps))
        for i in range(n_steps):
            boxcar_data[i] = np.mean(data[i*averaging_window:(i+1)*averaging_window], axis=0)

        return boxcar_data
            

    def perform_fft(self, data, title, label):

        for j in range(self.config.boxcar_avg_maxpow2 + 1):
            boxcar_averaging_window = int(math.pow(2, j))
            fft_data = self.boxcar_averaging(data, boxcar_averaging_window)
            fft = np.abs(np.fft.fft(fft_data))
            fft = fft[range(1, int(len(fft)/2))] # exclude the 0 Hz bin and the mirror symmetry data points
            
            freq_step = 1/(len(data)*constants.ring_revolution_period) # keep sample period to revolution
            frequencies = [int(i)*freq_step/1000 for i in range(0, len(fft))] # in from Hz to kHz
            
            boxcar_title = title +'\nboxcar ' + str(boxcar_averaging_window)
            fig, ax = plotting.create_figure(boxcar_title, 'Frequency [kHz]', 'FFT magnitude (log base 10)', self.config.data_file_tag[self.idx_file], self.config.timestamp)
            ax.set_yscale('log')
            ax.set_xlim(frequencies[0], frequencies[len(frequencies)-1])

            plt.grid(color='black', linestyle=':', linewidth=0.5, alpha=0.1)
            plt.grid(True)
            plt.plot(frequencies, fft)
            plt.savefig('results/'+ self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + label + '_boxcar' + str(boxcar_averaging_window) + '_fft.eps')
            plt.close()
        

    def vertical_centroid(self):

        if (self.config.verbose > 0 ):
            print('\n   ---------------------')
            print('   | Vertical centroid |')
            print('   ---------------------\n')

        self.vertical_centroid = []
        for i in range(self.config.n_turns):
            self.vertical_centroid.append(self.config.ky*(self.button[0][i]+self.button[3][i]-(self.button[1][i]+self.button[2][i]))/self.button_sum[i])

        for j in range(self.config.boxcar_avg_maxpow2 + 1):
            boxcar_averaging_window = int(math.pow(2, j))
            data = self.boxcar_averaging(np.array(self.vertical_centroid), boxcar_averaging_window)
            if (self.config.verbose > 0):
                printout.print_stat(data)
            # plot average subtracted raw button reading as a function of turn #
            boxcar_title = 'vertical centroid\nboxcar ' + str(boxcar_averaging_window)
            fig, ax = plotting.create_figure(boxcar_title, 'Turn #', 'Vertical centroid [mm] (mean subtracted)', self.config.data_file_tag[self.idx_file], self.config.timestamp)
            plt.plot([i for i in range(len(data))], data - np.mean(data))
            plt.savefig('results/' + self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + 'verticalCentroid_boxcar' +
                        str(boxcar_averaging_window) + '_trendAvgSubtracted.eps')
            plt.close()
            fig, ax = plotting.create_figure(boxcar_title, 'Turn #', 'Vertical centroid [mm]', self.config.data_file_tag[self.idx_file], self.config.timestamp)
            plt.plot([i for i in range(len(data))], data)
            plt.savefig('results/' + self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + 'verticalCentroid_boxcar' +
                        str(boxcar_averaging_window) + '_trend.eps')
            plt.close()

            boxcar_title = 'vertical centroid\nboxcar ' + str(boxcar_averaging_window)
            label = 'button' + str(i)
            fig, ax = plotting.create_figure(boxcar_title, 'Vertical centroid [mm]', '#', self.config.data_file_tag[self.idx_file], self.config.timestamp)
            intensity, bin_edge, _ = plt.hist(data, bins=int(math.sqrt(len(data))))
            plt.savefig('results/' + self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + 'verticalCentroid_boxcar' +
                        str(boxcar_averaging_window) + '_dist.eps')
            plt.close()

        self.mean_vertical_centroid =  np.mean(self.vertical_centroid)
        self.std_vertical_centroid =  np.std(self.vertical_centroid)
        self.perform_fft(self.vertical_centroid, 'vertical centroid', 'vertical_centroid')

    def horizontal_centroid(self):

        if (self.config.verbose > 0 ):
            print('\n   -----------------------')
            print('   | Horizontal centroid |')
            print('   -----------------------\n')

        self.horizontal_centroid = []
        for i in range(self.config.n_turns):
            self.horizontal_centroid.append(self.config.kx*(self.button[2][i]+self.button[3][i]-(self.button[1][i]+self.button[0][i]))/self.button_sum[i])

        for j in range(self.config.boxcar_avg_maxpow2 + 1):
            boxcar_averaging_window = int(math.pow(2, j))
            data = self.boxcar_averaging(np.array(self.horizontal_centroid), boxcar_averaging_window)
            if (self.config.verbose > 0):
                printout.print_stat(data)
            # plot average subtracted raw button reading as a function of turn #
            boxcar_title = 'horizontal centroid\nboxcar ' + str(boxcar_averaging_window)
            fig, ax = plotting.create_figure(boxcar_title, 'Turn #', 'Horizontal centroid [mm] (mean subtracted)', self.config.data_file_tag[self.idx_file], self.config.timestamp)
            plt.plot([i for i in range(len(data))], data - np.mean(data))
            plt.savefig('results/' + self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + 'horizontalCentroid_boxcar' + str(
                boxcar_averaging_window) + '_trendAvgSubtracted.eps')
            plt.close()
            fig, ax = plotting.create_figure(boxcar_title, 'Turn #', 'Horizontal centroid [mm]', self.config.data_file_tag[self.idx_file], self.config.timestamp)
            plt.plot([i for i in range(len(data))], data)
            plt.savefig('results/' + self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + 'horizontalCentroid_boxcar' + str(
                boxcar_averaging_window) + '_trend.eps')
            plt.close()

            boxcar_title = 'horizontal centroid\nboxcar ' + str(boxcar_averaging_window)
            fig, ax = plotting.create_figure(boxcar_title, 'Horizontal centroid [mm]', '#', self.config.data_file_tag[self.idx_file], self.config.timestamp)
            intensity, bin_edge, _ = plt.hist(data, bins=int(math.sqrt(len(data))))
            plt.savefig('results/' + self.config.cbpm[self.idx_cbpm] + '/' + self.config.data_file_tag[self.idx_file] + '/' + 'horizontalCentroid_boxcar' +
                        str(boxcar_averaging_window) + '_dist.eps')
            plt.close()

        self.mean_horizontal_centroid =  np.mean(self.horizontal_centroid)
        self.std_horizontal_centroid =  np.std(self.horizontal_centroid)
        self.perform_fft(self.horizontal_centroid, 'horizontal centroid', 'horizontal_centroid')